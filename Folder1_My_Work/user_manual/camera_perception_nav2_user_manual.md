# User Manual for Camera Perception, Road Following, and Nav2 Integration

## Purpose

This manual describes how to start and check my implemented subsystem for the IGVC Milk Dragon vehicle. The subsystem connects camera-based lane perception, lane projection, lane-target generation, front-sector LiDAR filtering, Nav2-based integration, and road-following behavior.

## My Work

The commands and components associated with my work include:

- Lane-perception stack
- Pixel-to-ground projection
- Lane-target generation
- Front-sector LiDAR filtering
- Nav2 bring-up support
- Road-following behavior
- Diagnostics and startup documentation

## Startup Order

The exact paths may be adjusted on the final competition computer, but the launch order should remain the same.

| Terminal | Command | Purpose | My Role |
|---|---|---|---|
| T1 | `ros2 launch milk_bringup sensor_all.launch.py` | Bring up sensors | Integration support |
| T1.5 | `ros2 run milk_bringup scan_front_filter` | Publish forward-sector `/scan_front` for Nav2 | Primary / integration |
| T2 | `ros2 launch lane_pixel_to_xyz lane_stack_nav2.launch.py pitch_deg:=12.0` | Start lane inference, projection, target generation, and diagnostics | Primary |
| T3 | `ros2 launch milk_bringup slam_toolbox.launch.py` | Start SLAM / mapping | Integration support |
| T4 / T5 | `p2os_driver + enable_motors` | Connect and enable the base | Team / support |
| T4.5 | `ros2 launch estop_pkg estop.launch.py` | Enable emergency-stop support | Team / support |
| T6 / T7 | `Nav2 + YOLO obstacle node` | Start local planning and obstacle topics | Integration support |
| T8 / T9 | `indoor_waypoint_nav + rviz2` | Run waypoint behavior and visualize the stack | Primary / integration |

## Required Checks Before Motion

Before running the robot, verify that the following topics or systems are available:

- `/kinect/image_raw` or the configured RGB image topic
- `/kinect/camera_info` or `/depth/camera_info`
- `/scan`
- `/scan_front`
- `/lane_target_point`
- `/lane_valid`
- `/local_costmap/costmap`
- `/cmd_vel`
- Motor enable status
- E-stop status

## Diagnostics Procedure

If lane behavior is missing:

1. Verify camera and LiDAR sensor topics.
2. Verify that the lane inference node is running.
3. Check left and right lane point cloud outputs.
4. Check projection parameters such as camera pose and `pitch_deg`.
5. Check `/lane_target_point` and `/lane_valid`.
6. Check Nav2 local costmap and `/scan_front`.
7. Check `/cmd_vel`, motor enable, and E-stop status.

## Notes

This subsystem should be started only after the basic sensor stack is active. Nav2 behavior should be started only after SLAM/map frames and managed Nav2 nodes are active.
