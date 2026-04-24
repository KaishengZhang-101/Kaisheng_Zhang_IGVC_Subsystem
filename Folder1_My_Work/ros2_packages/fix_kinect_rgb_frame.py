import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class FixKinectRgbFrame(Node):
    def __init__(self):
        super().__init__('fix_kinect_rgb_frame')

        self.declare_parameter('in_topic', '/kinect/image_raw')
        self.declare_parameter('out_topic', '/kinect/image_raw_fixed')
        self.declare_parameter('frame_id', 'camera_link')

        in_topic = self.get_parameter('in_topic').value
        out_topic = self.get_parameter('out_topic').value
        self.frame_id = self.get_parameter('frame_id').value

        self.pub = self.create_publisher(Image, out_topic, 10)
        self.sub = self.create_subscription(Image, in_topic, self.cb, 10)

        self.get_logger().info(f'Fix frame_id: {in_topic} -> {out_topic}, frame_id="{self.frame_id}"')

    def cb(self, msg: Image):
        if msg.header.frame_id is None or msg.header.frame_id.strip() == '':
            msg.header.frame_id = self.frame_id
        self.pub.publish(msg)

def main():
    rclpy.init()
    node = FixKinectRgbFrame()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
