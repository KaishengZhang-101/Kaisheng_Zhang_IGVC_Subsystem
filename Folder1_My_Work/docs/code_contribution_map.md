# Code Contribution Map

## Purpose

This file documents the code, launch files, configuration files, and external dependencies associated with my individual IGVC subsystem submission.

## Code Contribution Table

| Package / file group | Role | Authorship status | Notes |
|---|---|---|---|
| `lane_pixel_to_xyz.zip` | ROS 2 package archive for lane projection, target generation, diagnostics, and visualization | Primary subsystem work | Core deliverable of the winter term |
| `scan_front_filter.py` | Forward-sector LiDAR filter for Nav2 | Custom / modified integration node | Supports cleaner local costmaps |
| `indoor_waypoint_nav.py` | Road-following behavior with retries and costmap clearing | Primary / integration code | Used for navigation validation |
| `fix_kinect_rgb_frame.py` | Frame-consistency utility for Kinect RGB stream | Custom utility | Small but important integration fix |
| `scan_depth_fusion_node.py` | Depth / LiDAR fusion support | Collaborative / auxiliary | Helpful for near-obstacle monitoring |
| `lane_stack_nav2.launch.py` | Launch file for lane inference, projection, target generation, diagnostics, and Nav2-connected operation | Primary / integration | Used to start the implemented subsystem stack |
| `camera_projection_params.yaml` | Camera pose, pitch, and lane-target generation parameters | Primary / integration | Documents projection and calibration values used during testing |
| `nav2_integration_params.yaml` | Simplified Nav2 local costmap and controller integration parameters | Modified / integrated | Documents local costmap, controller, and topic interfaces |
| `kinect_ros2` | RGB-D driver package | Third-party reused package | External dependency, not claimed as original work |
| `lane_onnx` model package | Pretrained ONNX lane model and deployment wrapper | Integrated external model | Used as semantic front end rather than original model development |

## Configuration and Artifact Notes

- Launch files define both the base lane stack and the Nav2-connected variant used during integrated testing.
- Nav2 parameter files capture controller frequency, local costmap update rates, and obstacle-layer behavior relevant to this subsystem.
- Camera projection parameters document camera mounting, pitch angle, and lane-target generation assumptions.
- SLAM, EKF, and sensor configuration files support the larger vehicle architecture but are included as subsystem evidence because they affect lane integration and bring-up.
- Timeline figures, operating notes, and diagrams are retained as project-management and user-manual evidence.

## Notes on Authorship

Files marked as primary or custom are my individual or substantially modified work. Files marked as collaborative or third-party are included because they supported subsystem integration, testing, or deployment, but they are not claimed as fully original individual work.
