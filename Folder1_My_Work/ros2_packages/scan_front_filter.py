#!/usr/bin/env python3
"""
scan_front_filter.py (v3 — 干净版)

功能：
  1. 后方屏蔽：只保留前方 ±90° lidar 数据 → /scan_front 供 Nav2 costmap
  2. 前方测距日志：每 5 秒打印前方最近障碍距离和状态（调参用）
  3. 不碰 /cmd_vel — 避障完全由 Nav2 DWB 控制器处理

对比上一版改了什么：
  - 去掉了 Twist(0,0) 紧急停车 — 这是 "走走停停" 的根源
  - Nav2 的 DWB 控制器本身就有避障能力，不需要外部抢占
"""
import math
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

from sensor_msgs.msg import LaserScan


class ScanFrontFilter(Node):
    def __init__(self):
        super().__init__('scan_front_filter')

        self.declare_parameter('fov_deg', 180.0)
        self.declare_parameter('monitor_fov_deg', 80.0)
        self.declare_parameter('input_topic', '/scan')
        self.declare_parameter('output_topic', '/scan_front')
        self.declare_parameter('min_valid_range', 0.15)

        fov_deg = float(self.get_parameter('fov_deg').value)
        monitor_fov = float(self.get_parameter('monitor_fov_deg').value)
        self.half_fov = math.radians(fov_deg / 2.0)
        self.half_monitor = math.radians(monitor_fov / 2.0)
        self.min_range = float(self.get_parameter('min_valid_range').value)

        input_topic = str(self.get_parameter('input_topic').value)
        output_topic = str(self.get_parameter('output_topic').value)

        qos = QoSProfile(
            depth=5,
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            durability=DurabilityPolicy.VOLATILE,
        )

        self.sub = self.create_subscription(LaserScan, input_topic, self.cb, qos)
        self.pub = self.create_publisher(LaserScan, output_topic, qos)

        self._log_cnt = 0

        self.get_logger().info(
            f'scan_front_filter v3: {input_topic} -> {output_topic} '
            f'(costmap ±{fov_deg/2:.0f}度, 监控 ±{monitor_fov/2:.0f}度)'
        )

    def cb(self, msg: LaserScan):
        n = len(msg.ranges)
        if n == 0:
            return

        ranges = np.array(msg.ranges, dtype=np.float32)
        ranges[~np.isfinite(ranges)] = float('inf')
        ranges[ranges < self.min_range] = float('inf')

        angles = msg.angle_min + np.arange(n) * msg.angle_increment
        angles = np.arctan2(np.sin(angles), np.cos(angles))

        # 后方屏蔽
        ranges_out = ranges.copy()
        ranges_out[np.abs(angles) > self.half_fov] = float('inf')

        # 前方监控日志
        mask_front = np.abs(angles) <= self.half_monitor
        front_vals = ranges[mask_front]
        front_vals = front_vals[np.isfinite(front_vals)]
        front_min = float(np.min(front_vals)) if front_vals.size > 0 else float('inf')

        self._log_cnt += 1
        if self._log_cnt % 50 == 0:
            if front_min < 0.4:
                state = 'CRITICAL'
            elif front_min < 0.7:
                state = 'NEAR'
            elif front_min < 1.2:
                state = 'FAR'
            else:
                state = 'CLEAR'
            self.get_logger().info(f'[{state}] 前方最近 = {front_min:.2f}m')

        # 发布过滤 scan
        out = LaserScan()
        out.header = msg.header
        out.angle_min = msg.angle_min
        out.angle_max = msg.angle_max
        out.angle_increment = msg.angle_increment
        out.time_increment = msg.time_increment
        out.scan_time = msg.scan_time
        out.range_min = msg.range_min
        out.range_max = msg.range_max
        out.ranges = ranges_out.tolist()
        out.intensities = msg.intensities
        self.pub.publish(out)


def main():
    rclpy.init()
    node = ScanFrontFilter()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
