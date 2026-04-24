# Launch Files

This folder contains launch files associated with my individual subsystem work and integration testing.

## Main Launch File

| Launch file | Purpose | My role |
|---|---|---|
| `lane_stack_nav2.launch.py` | Starts the lane inference, projection, lane-target generation, diagnostics, and Nav2-connected perception stack | Primary / integration |

## Expected Usage

The main subsystem launch command used during testing was:

```bash
ros2 launch lane_pixel_to_xyz lane_stack_nav2.launch.py pitch_deg:=12.0
