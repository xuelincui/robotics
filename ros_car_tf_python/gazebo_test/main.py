#!/usr/bin/env python3
"""
Car acceleration controller — ROS 2 Jazzy + Gazebo Harmonic
"""

import subprocess, os
ros_setup = "/opt/ros/humble/setup.bash"
command = f"source {ros_setup} && env"
proc = subprocess.run(["bash", "-c", command], capture_output=True, text=True)
for line in proc.stdout.splitlines():
    if "=" in line:
        k, _, v = line.partition("=")
        os.environ[k] = v

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class CarController(Node):
    def __init__(self):
        super().__init__('car_controller')

        self.speed = 0.0
        self.position_x = 0.0
        self.commanded = 0.0
        self.target_speed = 10.0   # m/s
        self.accel_rate = 2.0      # m/s²
        self.dt = 0.1              # timer interval (seconds)
        self.state = 'accelerating'

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub = self.create_subscription(
            Odometry, '/odometry', self.odom_cb, 10)
        self.timer = self.create_timer(self.dt, self.control_loop)

        self.get_logger().info("=== Car Controller Started ===")
        self.get_logger().info(f"Target: {self.target_speed} m/s | Accel: {self.accel_rate} m/s²")

    def odom_cb(self, msg):
        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y
        self.speed = math.sqrt(vx**2 + vy**2)
        self.position_x = msg.pose.pose.position.x

    def send_velocity(self, speed):
        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = 0.0
        self.pub.publish(msg)

    def control_loop(self):
        if self.state == 'accelerating':
            self.commanded = min(
                self.commanded + self.accel_rate * self.dt,
                self.target_speed
            )
            self.send_velocity(self.commanded)
            self.get_logger().info(
                f"[ACCEL] Cmd: {self.commanded:.2f} m/s | "
                f"Actual: {self.speed:.2f} m/s | "
                f"Pos: {self.position_x:.2f} m"
            )
            if self.commanded >= self.target_speed:
                self.get_logger().info("Target speed reached! Cruising...")
                self.state = 'cruising'
                self.cruise_ticks = 0

        elif self.state == 'cruising':
            self.send_velocity(self.target_speed)
            self.cruise_ticks += 1
            if self.cruise_ticks >= 30:  # cruise for 3 seconds
                self.get_logger().info("Braking...")
                self.state = 'braking'

        elif self.state == 'braking':
            self.commanded = max(self.commanded - 3.0 * self.dt, 0.0)
            self.send_velocity(self.commanded)
            self.get_logger().info(
                f"[BRAKE] Cmd: {self.commanded:.2f} m/s | "
                f"Actual: {self.speed:.2f} m/s | "
                f"Pos: {self.position_x:.2f} m"
            )
            if self.commanded <= 0.0:
                self.get_logger().info("=== Stopped ===")
                self.state = 'done'

        elif self.state == 'done':
            self.send_velocity(0.0)


def main():
    rclpy.init()
    node = CarController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()