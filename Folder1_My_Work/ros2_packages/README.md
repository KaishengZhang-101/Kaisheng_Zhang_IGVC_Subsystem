# ROS 2 Packages and Nodes

This folder contains ROS 2 package-level code associated with my individual subsystem work.

## Main Package / Nodes

| Package or node | Purpose | My role |
|---|---|---|
| `lane_pixel_to_xyz.zip` | ROS 2 package archive for lane projection, target generation, diagnostics, and visualization | Primary subsystem work |
| `scan_front_filter.py` | Filters `/scan` into a forward-sector `/scan_front` topic for Nav2 local costmap use | Primary / modified integration |
| `indoor_waypoint_nav.py` | Runs waypoint-capable and road-following behavior using the deployed Nav2 stack | Primary / integration |
| `fix_kinect_rgb_frame.py` | Adds missing RGB frame metadata when needed | Custom utility |
| `scan_depth_fusion_node.py` | Supports depth / LiDAR obstacle monitoring | Collaborative / auxiliary |

## Expected Workspace Use

This build command is intended for the Ubuntu 22.04 / ROS 2 Humble robot computer, not directly for Windows.

The primary package can be placed into a ROS 2 workspace such as:

```bash
cd ~/milk_dragon_ws
colcon build --packages-select lane_pixel_to_xyz
source install/setup.bash
