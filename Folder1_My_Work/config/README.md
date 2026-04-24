# Configuration Files

This folder contains configuration files used or modified during my subsystem integration work.

## Configuration Summary

| File | Purpose | My role |
|---|---|---|
| `nav2_params.yaml` | Nav2 local costmap, controller frequency, and obstacle-layer parameters | Modified / integrated |
| `indoor_waypoints.yaml` | Waypoint behavior configuration used during indoor testing | Integration support |
| `camera_projection_params.yaml` | Camera pose and projection parameters such as camera position and pitch angle | Primary / integration |

## Important Parameters

The subsystem depends on several configuration values:

- `publish_hz = 10.0`
- `controller_frequency = 20 Hz`
- local costmap update rate
- local costmap publish rate
- camera pose parameters
- `pitch_deg`
- lookahead distance
- minimum points per lane boundary

## Notes

These files support the camera-perception, lane-projection, Nav2 local costmap, and road-following behavior described in the final report.
