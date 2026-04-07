#!/usr/bin/env python3
"""
Simple car acceleration simulation in Gazebo using ROS.
Requires: ROS (Noetic or Humble), Gazebo, and a car model with a drive plugin.
"""

import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math


class CarAccelerationSim:
    def __init__(self):
        rospy.init_node('car_acceleration_sim', anonymous=True)

        # --- Publishers ---
        # For a differential drive / Ackermann car model
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # If using wheel torque controllers directly:
        self.throttle_pub = rospy.Publisher('/vehicle/throttle', Float64, queue_size=10)

        # --- Subscribers ---
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)

        # --- State ---
        self.current_speed = 0.0
        self.current_x = 0.0
        self.target_speed = 0.0

        self.rate = rospy.Rate(10)  # 10 Hz control loop

    def odom_callback(self, msg):
        """Read current velocity from Gazebo odometry."""
        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y
        self.current_speed = math.sqrt(vx**2 + vy**2)
        self.current_x = msg.pose.pose.position.x

    def accelerate(self, target_speed, acceleration_rate=1.0):
        """
        Gradually accelerate the car to a target speed.

        :param target_speed: Desired speed in m/s
        :param acceleration_rate: Speed increase per second (m/s²)
        """
        rospy.loginfo(f"Accelerating to {target_speed} m/s at {acceleration_rate} m/s²")
        cmd = Twist()
        commanded_speed = 0.0

        while not rospy.is_shutdown():
            # Ramp up commanded speed
            if commanded_speed < target_speed:
                commanded_speed = min(
                    commanded_speed + acceleration_rate * 0.1,  # 0.1s per loop tick
                    target_speed
                )

            cmd.linear.x = commanded_speed
            cmd.angular.z = 0.0  # Drive straight
            self.cmd_vel_pub.publish(cmd)

            rospy.loginfo(
                f"Commanded: {commanded_speed:.2f} m/s | "
                f"Actual: {self.current_speed:.2f} m/s | "
                f"Position X: {self.current_x:.2f} m"
            )

            # Stop condition: reached target speed and traveled 20m
            if commanded_speed >= target_speed and self.current_x >= 20.0:
                rospy.loginfo("Target reached! Braking...")
                self.brake()
                break

            self.rate.sleep()

    def brake(self):
        """Bring the car to a stop."""
        cmd = Twist()
        cmd.linear.x = 0.0
        for _ in range(20):  # Publish stop for 2 seconds
            self.cmd_vel_pub.publish(cmd)
            self.rate.sleep()
        rospy.loginfo("Car stopped.")

    def run(self):
        rospy.sleep(1.0)  # Wait for Gazebo to initialize
        self.accelerate(target_speed=10.0, acceleration_rate=2.0)  # 0 → 10 m/s at 2 m/s²


if __name__ == '__main__':
    try:
        sim = CarAccelerationSim()
        sim.run()
    except rospy.ROSInterruptException:
        pass