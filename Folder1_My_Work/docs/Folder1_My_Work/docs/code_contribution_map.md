# Code Contribution Map

## Purpose

This file documents the code, launch files, configuration files, and external dependencies associated with my individual IGVC subsystem submission.

## Code Contribution Table

| Package / file group | Role | Authorship status | Notes |
|---|---|---|---|
| `lane_pixel_to_xyz` | Custom projection, target generation, diagnostics, and visualization | Primary subsystem work | Core deliverable of the winter term |
| `milk_tools/fix_kinect_rgb_frame.py` | Frame-consistency utility for Kinect RGB stream | Custom utility | Small but important integration fix |
| `milk_bringup/scan_front_filter.py` | Forward-sector LiDAR filter for Nav2 | Custom / modified integration node | Supports cleaner local costmaps |
| `milk_bringup/indoor_waypoint_nav.py` | Road-following behavior with retries and costmap clearing | Primary / integration code | Used for navigation validation |
| `milk_perception/scan_depth_fusion_node.py` | Depth / LiDAR fusion support | Collaborative | Helpful for near-obstacle monitoring |
| `kinect_ros2` | RGB-D driver package | Third-party reused package | External dependency, not claimed as original work |
| `lane_onnx` model package | Pretrained ONNX lane model and deployment wrapper | Integrated external model | Used as semantic front end rather than original model development |

## Configuration and Artifact Notes

- Launch files define both the base lane stack and the Nav2-connected variant used during integrated testing.
- Nav2 parameter files capture controller frequency, local costmap update rates, and obstacle-layer behavior relevant to this subsystem.
- SLAM, EKF, and sensor configuration files support the larger vehicle architecture but are included as subsystem evidence because they affect lane integration and bring-up.
- Timeline figures and operating notes are retained as project-management and user-manual evidence.
