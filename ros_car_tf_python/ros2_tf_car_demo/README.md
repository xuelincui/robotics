# ROS2 TF Car Motion Demo

Simulates a **car driving in a circle** and broadcasts a full TF2 frame tree.

## TF Frame Tree

```
world
└── base_link              ← car body (moves along circle)
    ├── front_left_wheel   ← spins (pitch) as car rolls
    ├── front_right_wheel
    ├── rear_left_wheel
    └── rear_right_wheel
```

## Topics Published

| Topic             | Type                      | Description                  |
|-------------------|---------------------------|------------------------------|
| `/tf`             | tf2_msgs/TFMessage        | Full TF tree (50 Hz)         |
| `/odom`           | nav_msgs/Odometry         | Car pose + velocity          |
| `/car/speed`      | std_msgs/Float32          | Linear speed [m/s]           |
| `/car/heading_deg`| std_msgs/Float32          | Heading angle [deg]          |

## Build & Run

```bash
# Copy into your workspace
cp -r ros2_tf_car_demo ~/ros2_ws/src/

cd ~/ros2_ws
colcon build --packages-select ros2_tf_car_demo
source install/setup.bash

# Option A — launch both nodes at once
ros2 launch ros2_tf_car_demo car_demo.launch.py

# Option B — run separately (separate terminals)
ros2 run ros2_tf_car_demo car_tf_broadcaster
ros2 run ros2_tf_car_demo car_tf_listener
```

## Visualise in RViz2

```bash
ros2 run rviz2 rviz2
```

In RViz2:
1. Set **Fixed Frame** → `world`
2. Add **TF** display → see all 5 frames animate
3. Add **Odometry** display → topic `/odom`

## Inspect via CLI

```bash
# See the TF tree
ros2 run tf2_tools view_frames

# Print a live transform (world → front_left_wheel)
ros2 run tf2_ros tf2_echo world front_left_wheel

# List all active frames
ros2 run tf2_ros tf2_monitor
```

## Key ROS2 / TF2 Concepts Demonstrated

| Concept | Where |
|---|---|
| `TransformBroadcaster.sendTransform()` | `car_tf_broadcaster.py` |
| Quaternion from Euler angles | `euler_to_quaternion()` helper |
| Child transforms (wheel rel. to body) | 4 wheel `sendTransform` calls |
| `tf2_ros.Buffer` + `TransformListener` | `car_tf_listener.py` |
| `lookup_transform()` across frames | `_lookup()` helper |
| Publishing `nav_msgs/Odometry` | `car_tf_broadcaster.py` |
| Launch file combining two nodes | `launch/car_demo.launch.py` |
