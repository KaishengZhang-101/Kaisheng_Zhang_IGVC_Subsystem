"""
lane_stack_nav2.launch.py
跟 lane_stack.launch.py 一样，但去掉了 lane_follow_controller
因为现在由 Nav2 控制 /cmd_vel
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    ros_domain_id = LaunchConfiguration('ros_domain_id')
    image_topic = LaunchConfiguration('image_topic')
    depth_topic = LaunchConfiguration('depth_topic')
    depth_info_topic = LaunchConfiguration('depth_info_topic')

    publish_hz = LaunchConfiguration('publish_hz')
    max_points_per_lane = LaunchConfiguration('max_points_per_lane')
    model_type = LaunchConfiguration('model_type')
    model_path = LaunchConfiguration('model_path')

    # ground-projection args
    output_frame = LaunchConfiguration('output_frame')
    camera_x = LaunchConfiguration('camera_x')
    camera_y = LaunchConfiguration('camera_y')
    camera_z = LaunchConfiguration('camera_z')
    pitch_deg = LaunchConfiguration('pitch_deg')
    ground_z = LaunchConfiguration('ground_z')
    max_range = LaunchConfiguration('max_range')

    lane_onnx_share = get_package_share_directory('lane_onnx')
    default_model = os.path.join(lane_onnx_share, 'models', 'lane.onnx')

    return LaunchDescription([
        DeclareLaunchArgument('ros_domain_id', default_value='0'),
        DeclareLaunchArgument('image_topic', default_value='/kinect/image_raw'),
        DeclareLaunchArgument('depth_topic', default_value='/kinect/depth/image_raw'),
        DeclareLaunchArgument('depth_info_topic', default_value='/kinect/depth/camera_info'),

        DeclareLaunchArgument('publish_hz', default_value='10.0'),
        DeclareLaunchArgument('max_points_per_lane', default_value='30'),
        DeclareLaunchArgument('model_type', default_value='tusimple'),
        DeclareLaunchArgument('model_path', default_value=default_model),

        # base_link mounting parameters for lane ground projection
        DeclareLaunchArgument('output_frame', default_value='base_link'),
        DeclareLaunchArgument('camera_x', default_value='0.199'),
        DeclareLaunchArgument('camera_y', default_value='0.0'),
        DeclareLaunchArgument('camera_z', default_value='0.726'),
        DeclareLaunchArgument('pitch_deg', default_value='0.0'),
        DeclareLaunchArgument('ground_z', default_value='0.0'),
        DeclareLaunchArgument('max_range', default_value='1.5'),  # lane点云最大前方距离(m)

        SetEnvironmentVariable('ROS_DOMAIN_ID', ros_domain_id),

        # ① 车道线 ONNX 检测
        Node(
            package='lane_onnx',
            executable='lane_onnx_node',
            name='lane_onnx',
            output='screen',
            parameters=[{
                'model_path': model_path,
                'model_type': model_type,
                'publish_hz': publish_hz,
                'max_points_per_lane': max_points_per_lane,
            }],
            remappings=[
                ('/image_raw', image_topic),
            ]
        ),

        # ② 像素 → 3D 点云 (带地面投影参数)
        Node(
            package='lane_pixel_to_xyz',
            executable='pixel_to_xyz',
            name='pixel_to_xyz',
            output='screen',
            parameters=[{
                'output_frame': output_frame,
                'camera_x': camera_x,
                'camera_y': camera_y,
                'camera_z': camera_z,
                'pitch_deg': pitch_deg,
                'ground_z': ground_z,
                'max_range': max_range,
            }],
            remappings=[
                ('/depth/image_raw', depth_topic),
                ('/camera_info', depth_info_topic),
            ]
        ),

        # ③ 车道中点计算
        Node(
            package='lane_pixel_to_xyz',
            executable='lane_target_from_xyz',
            name='lane_target_from_xyz',
            output='screen',
            parameters=[{
                'left_topic': '/lane_left_points_xyz',
                'right_topic': '/lane_right_points_xyz',
                'target_topic': '/lane_target_point',
                'valid_topic': '/lane_valid',
                'output_frame': output_frame,
                'lookahead_x': 1.2,
                'window_half_width': 0.35,
                'min_points_per_side': 2,
            }]
        ),

        # ❌ 去掉了 lane_follow_controller — Nav2 现在控制 /cmd_vel

        # ④ Motor controller: Nav2 的 /cmd_vel → P2OS
        Node(
            package='lane_pixel_to_xyz',
            executable='motor_controller',
            name='motor_controller',
            output='screen',
            parameters=[{
                'input_topic': '/cmd_vel',
                'output_topic': '/cmd_vel',
                'motor_enable': True,
                'max_linear_vel': 0.5,
                'max_angular_vel': 1.0,
            }]
        ),

        # ⑤ 诊断
        Node(
            package='lane_pixel_to_xyz',
            executable='stack_diagnostics',
            name='stack_diagnostics',
            output='screen',
            parameters=[{'check_interval': 2.0}]
        ),

        # ⑥ 可视化
        Node(
            package='lane_pixel_to_xyz',
            executable='lane_visualizer',
            name='lane_visualizer',
            output='screen',
        ),
    ])
