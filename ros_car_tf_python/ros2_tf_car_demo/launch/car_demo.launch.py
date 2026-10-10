"""
car_demo.launch.py — starts broadcaster + listener together

    ros2 launch ros2_tf_car_demo car_demo.launch.py

    Step 1: Build from the workspace root
    bashcd ~/repo/robotics/ros_car_tf_python
    colcon build --packages-select ros2_tf_car_demo

    Step 2: Source the install setup
    bashsource install/setup.bash


    Step 3: Now launch
    bashros2 launch ros2_tf_car_demo car_demo.launch.py

"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros2_tf_car_demo',
            executable='car_tf_broadcaster',
            name='car_tf_broadcaster',
            output='screen',
        ),
        Node(
            package='ros2_tf_car_demo',
            executable='car_tf_listener',
            name='car_tf_listener',
            output='screen',
        ),
    ])
