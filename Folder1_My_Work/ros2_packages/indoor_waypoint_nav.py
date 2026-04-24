#!/usr/bin/env python3
"""
室内航点导航 (v4 — 增加重试 + 位置监控)

改动对比 v3：
  1. Nav2 abort 后不再直接跳过，而是重试最多 3 次
  2. 每次重试前清空 costmap（防止残留障碍堵路）
  3. 订阅 /odom 实时打印机器人位置（方便确认到底走到哪了）
  4. 导航中每 5 秒打印一次距离目标的剩余距离
"""
import math
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from nav2_msgs.srv import ClearEntireCostmap
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
import yaml


class IndoorWaypointNav(Node):
    def __init__(self):
        super().__init__('indoor_waypoint_nav')

        self.declare_parameter('waypoints_file', '')
        self.declare_parameter('return_to_start', True)
        self.declare_parameter('wait_at_waypoint', 3.0)
        self.declare_parameter('max_retries', 3)

        self.waypoints_file = self.get_parameter('waypoints_file').value
        self.return_to_start = self.get_parameter('return_to_start').value
        self.wait_time = self.get_parameter('wait_at_waypoint').value
        self.max_retries = int(self.get_parameter('max_retries').value)

        # Nav2 action client
        self.nav_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Costmap clear 服务（重试前清空残留障碍）
        self.clear_local = self.create_client(
            ClearEntireCostmap, '/local_costmap/clear_entirely_local_costmap')
        self.clear_global = self.create_client(
            ClearEntireCostmap, '/global_costmap/clear_entirely_global_costmap')

        # 位置监控
        self.robot_x = 0.0
        self.robot_y = 0.0
        self.robot_yaw = 0.0
        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)

        # 状态
        self.all_waypoints = []
        self.current_index = 0
        self.retry_count = 0
        self.busy = False
        self.wait_timer = None
        self.monitor_timer = None

        self.get_logger().info('室内航点导航启动 (v4 — 带重试)')
        self.get_logger().info(f'  回到原点: {self.return_to_start}')
        self.get_logger().info(f'  航点等待: {self.wait_time}s')
        self.get_logger().info(f'  最大重试: {self.max_retries}次')

        self._start_timer = self.create_timer(3.0, self.start_navigation)
        self._started = False

    def odom_cb(self, msg: Odometry):
        self.robot_x = msg.pose.pose.position.x
        self.robot_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.robot_yaw = math.atan2(
            2.0 * (q.w * q.z + q.x * q.y),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        )

    def start_navigation(self):
        if self._started:
            return
        self._started = True
        self._start_timer.cancel()

        self.get_logger().info('等待 Nav2...')
        if not self.nav_client.wait_for_server(timeout_sec=10.0):
            self.get_logger().error('Nav2 连接超时！')
            return
        self.get_logger().info('✅ Nav2 已连接')

        waypoints = self.load_waypoints()
        if not waypoints:
            self.get_logger().error('没有航点！')
            return

        self.all_waypoints = waypoints
        if self.return_to_start:
            self.all_waypoints.append({'x': 0.0, 'y': 0.0, 'yaw': 0.0, 'name': '原点'})

        # 打印完整路径
        self.get_logger().info(f'🚀 开始导航 {len(self.all_waypoints)} 个航点:')
        for i, wp in enumerate(self.all_waypoints):
            name = wp.get('name', f'航点{i+1}')
            self.get_logger().info(f'   {i+1}. {name} ({wp["x"]}, {wp["y"]})')

        self.current_index = 0
        self.retry_count = 0
        self.send_next_goal()

    def load_waypoints(self):
        if not self.waypoints_file:
            self.get_logger().error('没有指定 waypoints_file')
            return []
        try:
            with open(self.waypoints_file, 'r') as f:
                data = yaml.safe_load(f)
            return data.get('waypoints', [])
        except Exception as e:
            self.get_logger().error(f'读取航点失败: {e}')
            return []

    def clear_costmaps(self):
        """清空 costmap 残留障碍"""
        req = ClearEntireCostmap.Request()
        if self.clear_local.service_is_ready():
            self.clear_local.call_async(req)
        if self.clear_global.service_is_ready():
            self.clear_global.call_async(req)
        self.get_logger().info('🧹 已清空 costmap')

    def send_next_goal(self):
        if self.current_index >= len(self.all_waypoints):
            self.stop_monitor()
            self.get_logger().info('🎉 所有航点导航完成！')
            self.get_logger().info(
                f'   最终位置: ({self.robot_x:.2f}, {self.robot_y:.2f})')
            self.busy = False
            return

        if self.busy:
            return
        self.busy = True

        wp = self.all_waypoints[self.current_index]
        x = float(wp['x'])
        y = float(wp['y'])
        yaw = float(wp.get('yaw', 0.0))
        name = wp.get('name', f'航点{self.current_index + 1}')

        dist = math.hypot(x - self.robot_x, y - self.robot_y)
        retry_str = f' (重试 {self.retry_count}/{self.max_retries})' if self.retry_count > 0 else ''

        self.get_logger().info(f'')
        self.get_logger().info(f'{"="*50}')
        self.get_logger().info(
            f'🎯 导航到 {name} ({self.current_index + 1}/{len(self.all_waypoints)}){retry_str}')
        self.get_logger().info(f'   目标: ({x:.2f}, {y:.2f})  当前: ({self.robot_x:.2f}, {self.robot_y:.2f})  距离: {dist:.2f}m')
        self.get_logger().info(f'{"="*50}')

        goal = NavigateToPose.Goal()
        goal.pose = PoseStamped()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.position.z = 0.0
        goal.pose.pose.orientation.z = math.sin(yaw / 2.0)
        goal.pose.pose.orientation.w = math.cos(yaw / 2.0)

        # 启动距离监控
        self.start_monitor()

        send_future = self.nav_client.send_goal_async(goal)
        send_future.add_done_callback(self.goal_response_cb)

    def start_monitor(self):
        """每5秒打印一次到目标距离"""
        self.stop_monitor()
        self.monitor_timer = self.create_timer(5.0, self.monitor_cb)

    def stop_monitor(self):
        if self.monitor_timer is not None:
            self.monitor_timer.cancel()
            self.monitor_timer = None

    def monitor_cb(self):
        if self.current_index >= len(self.all_waypoints):
            self.stop_monitor()
            return
        wp = self.all_waypoints[self.current_index]
        gx, gy = float(wp['x']), float(wp['y'])
        dist = math.hypot(gx - self.robot_x, gy - self.robot_y)
        name = wp.get('name', f'航点{self.current_index + 1}')
        self.get_logger().info(
            f'   📍 {name} 剩余 {dist:.2f}m  当前位置: ({self.robot_x:.2f}, {self.robot_y:.2f})')

    def goal_response_cb(self, future):
        goal_handle = future.result()
        if not goal_handle or not goal_handle.accepted:
            name = self.all_waypoints[self.current_index].get('name', f'航点{self.current_index + 1}')
            self.get_logger().warn(f'⚠️ {name} 被 Nav2 拒绝')
            self.handle_failure()
            return

        self.get_logger().info('Nav2 接受目标，导航中...')
        self._current_goal_handle = goal_handle
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_cb)

    def result_cb(self, future):
        self.stop_monitor()

        if self.current_index >= len(self.all_waypoints):
            return

        wp = self.all_waypoints[self.current_index]
        name = wp.get('name', f'航点{self.current_index + 1}')
        gx, gy = float(wp['x']), float(wp['y'])
        dist = math.hypot(gx - self.robot_x, gy - self.robot_y)

        result = future.result()
        if result.status == 4:  # SUCCEEDED
            self.get_logger().info(
                f'✅ 到达 {name}！（误差 {dist:.2f}m）等待 {self.wait_time}s...')
            self.busy = False
            self.current_index += 1
            self.retry_count = 0
            self.schedule_next()
        elif result.status == 6:  # ABORTED
            self.get_logger().warn(
                f'⚠️ {name} 导航被中止 (距目标还有 {dist:.2f}m)')
            self.handle_failure()
        else:
            self.get_logger().warn(
                f'⚠️ {name} 导航结束 status={result.status} (距目标 {dist:.2f}m)')
            self.handle_failure()

    def handle_failure(self):
        """失败处理：重试或跳过"""
        name = self.all_waypoints[self.current_index].get('name', f'航点{self.current_index + 1}')

        if self.retry_count < self.max_retries:
            self.retry_count += 1
            self.get_logger().info(
                f'🔄 重试 {name} ({self.retry_count}/{self.max_retries})，先清空 costmap...')
            self.clear_costmaps()
            self.busy = False
            # 等 2 秒让 costmap 重建，再重试
            if self.wait_timer is not None:
                self.wait_timer.cancel()
            self.wait_timer = self.create_timer(2.0, self._on_retry)
        else:
            self.get_logger().error(
                f'❌ {name} 重试 {self.max_retries} 次仍失败，跳过')
            self.busy = False
            self.current_index += 1
            self.retry_count = 0
            self.schedule_next()

    def _on_retry(self):
        if self.wait_timer is not None:
            self.wait_timer.cancel()
            self.wait_timer = None
        self.send_next_goal()

    def schedule_next(self):
        if self.wait_timer is not None:
            self.wait_timer.cancel()
        self.wait_timer = self.create_timer(self.wait_time, self._on_wait_done)

    def _on_wait_done(self):
        if self.wait_timer is not None:
            self.wait_timer.cancel()
            self.wait_timer = None
        self.send_next_goal()


def main():
    rclpy.init()
    node = IndoorWaypointNav()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
