# Collaborative Integration Notes

## Purpose

This file documents collaborative vehicle-level integration work that supported my individual subsystem. These items are not claimed as fully individual code, but they were required for full-system testing and bring-up.

## Vehicle-Level Dependencies

My subsystem depended on the following full-vehicle components:

| Component | Purpose | My role |
|---|---|---|
| Sensor bring-up | Starts camera, LiDAR, and other sensor topics | Integration support |
| SLAM / mapping | Provides map frame and map output for navigation | Integration support |
| Nav2 stack | Provides navigation services, local planner, local costmap, and `/cmd_vel` output | Integration support |
| Base driver | Connects motion commands to the robot base | Team / support |
| E-stop system | Provides safety interlock during robot testing | Team / support |
| RViz visualization | Used for checking map, local costmap, lane output, and frames | Integration support |

## Integration Sequence Used During Testing

The integrated robot stack was normally brought up in this order:

1. Start sensors.
2. Start lane perception and projection stack.
3. Start SLAM / mapping.
4. Start the base driver and enable motors.
5. Start E-stop support.
6. Start Nav2.
7. Start waypoint or road-following behavior.
8. Use RViz to verify map, costmap, lane target, and motion command output.

## My Integration Role

My main integration role was connecting the camera-perception subsystem to the deployed robot stack. This included:

- Checking camera and LiDAR topic availability.
- Connecting projected lane geometry to downstream navigation behavior.
- Supporting `/scan_front` use for forward-sector obstacle filtering.
- Checking local costmap visualization in RViz.
- Debugging frame, launch, and topic issues.
- Documenting the startup order required for repeatable subsystem testing.

## Notes on Authorship

This file documents collaborative system-level integration. It does not claim full authorship of all vehicle-level components.
