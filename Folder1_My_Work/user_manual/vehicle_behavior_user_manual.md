# Vehicle Behavior User Manual

## Purpose

This manual documents the vehicle behaviors that I wrote or integrated for the IGVC Milk Dragon vehicle. These behaviors connect lane perception, lane-target generation, front-sector obstacle filtering, Nav2-based waypoint execution, and diagnostics.

## Behavior Summary

| Vehicle behavior | Related node / command | Input / state | Output / effect | My role |
|---|---|---|---|---|
| Road-following behavior | `indoor_waypoint_nav` / road-following logic | `/lane_target_point`, `/lane_valid`, Nav2 state | Commands the robot to follow lane-centered targets during integrated operation | Primary / integration |
| Lane-target generation | `lane_target_from_xyz` | left/right lane point clouds | Publishes `/lane_target_point` and `/lane_valid` | Primary |
| Front-sector obstacle filtering | `scan_front_filter.py` | `/scan` | Publishes `/scan_front` for forward obstacle awareness | Primary / modified integration |
| Nav2-based waypoint execution | `indoor_waypoint_nav` after Nav2 activation | map, odom, Nav2 managed nodes | Runs waypoint-capable operation through the deployed Nav2 stack | Primary / integration |
| RGB frame consistency behavior | `fix_kinect_rgb_frame.py` | Kinect RGB image stream | Fills missing frame metadata to prevent visualization / integration failures | Custom utility |
| Integrated stack diagnostics | `stack_diagnostics` | lane, scan, motion, and Nav2 topics | Reports missing topics or launch failures during bring-up | Primary / support |

## Road-Following Behavior

The road-following behavior uses the lane target generated from camera perception and connects it with the deployed Nav2-based stack. The behavior should only run after the sensors, lane stack, SLAM, Nav2, and base driver are active.

### Inputs

- `/lane_target_point`
- `/lane_valid`
- map / odom state
- Nav2 managed node state

### Expected Effect

The robot should follow lane-centered targets during integrated operation while still using the deployed Nav2-based navigation stack and local costmap information.

## Lane-Target Generation

The lane-target generation behavior converts left and right lane point clouds into a usable center target.

### Inputs

- Left lane point cloud
- Right lane point cloud

### Outputs

- `/lane_target_point`
- `/lane_valid`

### Validity Rule

A target should only be produced when both lane boundaries contain enough valid points. This avoids unstable centerline commands from sparse or false detections.

## Front-Sector Obstacle Filtering

The front-sector LiDAR filter restricts LiDAR input to the forward driving sector.

### Input

- `/scan`

### Output

- `/scan_front`

### Purpose

This reduces irrelevant scan returns behind the robot and provides cleaner obstacle information for Nav2 local costmap integration.

## RGB Frame Consistency Behavior

The RGB frame consistency utility fills missing frame metadata when needed.

### Purpose

This prevents visualization and integration failures caused by missing image frame information.

## Integrated Diagnostics

The diagnostics behavior checks key topics and launch status during bring-up.

### Checks

- Camera topic availability
- LiDAR topic availability
- Lane point cloud outputs
- Lane target output
- `/scan_front`
- Nav2 local costmap
- `/cmd_vel`
- Motor enable and E-stop status
