# milk_perception/scan_depth_fusion_node.py
# 功能：近似时间同步 /scan 与 /kinect/depth/image_raw
# 发布：
#   /min_obstacle_range_fused (Float32)  - 融合后的最小距离（雷达 vs 中心ROI深度，取较小者）
#   /min_depth_center         (Float32)  - 深度图中心窗口的最小深度
#   /fusion_debug_front       (Float32)  - 雷达前向扇区（±front_half_angle）最小距离，调参用
import math
import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan, Image
import message_filters

def _clean_ranges(ranges):
    return [r for r in ranges if (r is not None and math.isfinite(r) and r > 0.0)]

class ScanDepthFusion(Node):
    def __init__(self):
        super().__init__('scan_depth_fusion')

        # 可调参数
        self.declare_parameter('scan_topic', '/scan')
        self.declare_parameter('depth_topic', '/kinect/depth/image_raw')
        self.declare_parameter('front_half_angle_deg', 20.0)  # 雷达前向扇区半角
        self.declare_parameter('depth_center_window', 0.2)    # 取图像宽/高的 20% 中心方窗
        self.declare_parameter('max_depth_clip', 5.0)         # 深度上限裁剪（米）

        self.front_half_angle = math.radians(float(self.get_parameter('front_half_angle_deg').value))
        self.center_window = float(self.get_parameter('depth_center_window').value)
        self.max_depth = float(self.get_parameter('max_depth_clip').value)

        scan_topic = self.get_parameter('scan_topic').value
        depth_topic = self.get_parameter('depth_topic').value

        # 近似时间同步
        self.scan_sub  = message_filters.Subscriber(self, LaserScan, scan_topic)
        self.depth_sub = message_filters.Subscriber(self, Image,    depth_topic)
        sync = message_filters.ApproximateTimeSynchronizer(
            [self.scan_sub, self.depth_sub], queue_size=10, slop=0.1
        )
        sync.registerCallback(self.cb_sync)

        # 发布者
        self.pub_min_fused  = self.create_publisher(Float32, '/min_obstacle_range_fused', 10)
        self.pub_min_center = self.create_publisher(Float32, '/min_depth_center', 10)
        self.pub_front_debug= self.create_publisher(Float32, '/fusion_debug_front', 10)

        self.get_logger().info(
            f'Fusion node on scan="{scan_topic}", depth="{depth_topic}", '
            f'front_half_angle={math.degrees(self.front_half_angle):.1f} deg, '
            f'center_window={self.center_window:.2f}, max_depth={self.max_depth:.1f}m'
        )

    def cb_sync(self, scan_msg: LaserScan, depth_msg: Image):
        # 1) 雷达：全场 & 前向扇区最小值
        valid = _clean_ranges(scan_msg.ranges)
        min_scan_all = min(valid) if valid else float('inf')

        def ang_to_idx(a):
            return int(round((a - scan_msg.angle_min) / scan_msg.angle_increment))
        i0 = max(0, min(len(scan_msg.ranges)-1, ang_to_idx(-self.front_half_angle)))
        i1 = max(0, min(len(scan_msg.ranges)-1, ang_to_idx(+self.front_half_angle)))
        if i0 > i1:
            i0, i1 = i1, i0
        front_slice = _clean_ranges(scan_msg.ranges[i0:i1+1])
        min_scan_front = min(front_slice) if front_slice else float('inf')
        self.pub_front_debug.publish(Float32(data=float(min_scan_front)))

        # 2) 深度：中心窗口最小值
        w, h = depth_msg.width, depth_msg.height
        ww = max(1, int(w * self.center_window))
        hh = max(1, int(h * self.center_window))
        x0 = (w - ww)//2; x1 = x0 + ww
        y0 = (h - hh)//2; y1 = y0 + hh

        if depth_msg.encoding in ('16UC1', 'mono16'):
            # 多数 16UC1 是毫米，按毫米→米；若你的驱动本来就是米，去掉 /1000.0
            arr = np.frombuffer(depth_msg.data, dtype=np.uint16).reshape(h, w).astype(np.float32) / 1000.0
        else:
            # 常见 32FC1，单位米
            arr = np.frombuffer(depth_msg.data, dtype=np.float32).reshape(h, w)

        roi = arr[y0:y1, x0:x1]
        roi = roi[np.isfinite(roi)]
        roi = roi[(roi > 0.0) & (roi < self.max_depth)]
        min_depth_center = float(np.min(roi)) if roi.size > 0 else float('inf')
        self.pub_min_center.publish(Float32(data=min_depth_center))

        # 3) 融合：取更保守的较小值
        min_fused = float(min(min_scan_all, min_depth_center))
        self.pub_min_fused.publish(Float32(data=min_fused))

def main(args=None):
    rclpy.init(args=args)
    node = ScanDepthFusion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
