# Drawings and System Diagrams

This folder contains schematic-style system diagrams associated with my subsystem work.

The subsystem did not require a new electrical schematic. Instead, the drawings document the software and integration architecture used to connect camera perception, lane projection, front-sector LiDAR filtering, Nav2, and road-following behavior.

## Included Drawings

| Drawing | Description | My update |
|---|---|---|
| `perception_to_navigation_signal_chain.png` | Shows camera image input, lane inference, pixel projection, lane-target generation, and Nav2 integration | Added lane-to-ground projection and lane-target generation stages |
| `nav2_local_costmap_integration.png` | Shows `/scan_front`, camera obstacle topics, map, odom, Nav2 local costmap, and `/cmd_vel` connection | Added front-sector LiDAR filtering and local-costmap connection |

## Notes

These diagrams correspond to the system drawings included in Appendix C of the final report.
