# Folder1 - My Work

This folder contains my primary individual work for the IGVC subsystem.

## Subsystem

Camera Perception, Road Following, and Nav2-Based System Integration for an IGVC Autonomous Ground Vehicle

## Included Work

- User manual for the camera-perception and Nav2-integration subsystem.
- User manual for vehicle behaviors that I wrote or integrated.
- ROS 2 code related to lane projection, target generation, front-sector LiDAR filtering, road-following, and diagnostics.
- Launch files and configuration files required to run the subsystem.
- System diagrams and schematic-style drawings that document the subsystem architecture.

## Main Contributions

| File or folder | Description | Authorship |
|---|---|---|
| `lane_pixel_to_xyz/` | Lane projection, target generation, diagnostics, and visualization | Primary subsystem work |
| `scan_front_filter.py` | Forward-sector LiDAR filtering for Nav2/local costmap use | Primary / modified integration |
| `indoor_waypoint_nav.py` | Road-following and waypoint-capable behavior | Primary / integration |
| `fix_kinect_rgb_frame.py` | Utility for RGB frame consistency | Custom utility |
| `lane_stack_nav2.launch.py` | Launch file for lane stack and Nav2-connected operation | Primary / integration |
| `nav2_params.yaml` | Nav2 local costmap and controller parameters used during integration | Modified / integrated |
