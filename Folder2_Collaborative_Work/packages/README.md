# Collaborative Packages and Dependencies

This folder contains collaborative vehicle-level packages and reused dependencies that supported full-system testing.

These files are not all claimed as fully original individual work. They are included because my subsystem depended on them during integration, testing, bring-up, or validation.

## Package Summary

| Package archive | Purpose | My role |
|---|---|---|
| `milk_bringup.zip` | Vehicle bring-up, launch files, sensor startup, SLAM/Nav2 integration support | Integration support |
| `milk_perception.zip` | Perception support including depth / LiDAR fusion or obstacle-related perception nodes | Collaborative / auxiliary |
| `camera_detect.zip` | Camera-based obstacle or detection support package | Collaborative / auxiliary |
| `lidar_obstacle_detection_tracking.zip` | LiDAR obstacle detection / tracking support | Collaborative / auxiliary |
| `lane_onnx.zip` | Pretrained ONNX lane model package or deployment wrapper | Integrated external model |
| `kinect_ros2.zip` | Kinect RGB-D driver package | Third-party reused package |

## Notes on Authorship

Only my direct integration, testing, documentation, or subsystem connection work is claimed here. Third-party or collaborative packages are included as dependencies and supporting materials, not as fully original individual code.
