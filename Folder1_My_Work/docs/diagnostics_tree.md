# Diagnostics Tree for Camera Perception and Nav2 Integration

## Purpose

This diagnostics tree is used to debug the implemented subsystem from sensor input to robot motion output.

Signal chain:

Sensor input → lane inference → geometric projection → lane-target generation → Nav2 integration → motion command output

## 1. Sensor Availability

If lane behavior is missing, first check sensor topics.

Required checks:

- `/kinect/image_raw` or configured RGB image topic
- `/kinect/depth/image_raw`
- `/kinect/camera_info` or `/depth/camera_info`
- `/scan`
- `/scan_front`

If these topics are missing, restart the sensor launch file before debugging higher-level nodes.

## 2. Lane Inference

If sensors are available but lane output is missing:

- Confirm that the lane inference node is running.
- Check `/lane_left_points_xyz`.
- Check `/lane_right_points_xyz`.
- Inspect ONNX inference node, image topic remapping, and launch parameters.

## 3. Projection Stage

If lane clouds exist but appear in the wrong location:

- Verify camera intrinsics from `camera_info`.
- Verify camera mounting parameters.
- Check `camera_x`, `camera_z`, and `pitch_deg`.
- Inspect projected lane points in RViz.
- Recalibrate pitch and camera pose if the lane projection appears shifted or floating.

## 4. Lane-Target Generation

If lane clouds are valid but the robot does not generate a stable target:

- Inspect `/lane_target_point`.
- Inspect `/lane_valid`.
- Confirm both lane boundaries contain enough valid points.
- Check minimum point threshold.
- Check lookahead distance.

If only one boundary is detected, the system should reject the target rather than generate an unstable centerline.

## 5. Nav2 and Costmap Integration

If the lane target is valid but navigation behavior is poor:

- Inspect `/local_costmap/costmap` in RViz.
- Verify `/scan_front` is being used for forward obstacle filtering.
- Check whether obstacle layers are over-blocking the local planner.
- Tune costmap range, obstacle marking, and local planner parameters if Nav2 stalls or oscillates.

## 6. Motion Command Chain

If perception and Nav2 are valid but the robot does not move:

- Verify `/cmd_vel`.
- Verify that `motor_controller` receives `/cmd_vel`.
- Verify that commands are forwarded to `/p2os_driver/cmd_vel`.
- Check motor enable status.
- Check E-stop status.
- Check base-driver connection.

## 7. Launch Order

If the full stack fails during startup:

1. Start sensors.
2. Start lane stack and projection nodes.
3. Start SLAM and confirm the map frame.
4. Start Nav2 and wait until managed nodes are active.
5. Start waypoint or road-following behavior only after Nav2 is active.
