"""
car_tf_broadcaster.py — ROS2 TF2 Car Motion Demo

Simulates a car driving in a circle and broadcasts the full TF tree:

    world
    └── base_link          (car body — moves in a circle)
        ├── front_left_wheel
        ├── front_right_wheel
        ├── rear_left_wheel
        └── rear_right_wheel

Also publishes:
  • /odom            (nav_msgs/Odometry)  — for RViz2 visualisation
  • /car/speed       (std_msgs/Float32)   — current linear speed [m/s]
  • /car/heading_deg (std_msgs/Float32)   — heading angle [deg]

Run with:
    ros2 run ros2_tf_car_demo car_tf_broadcaster

Visualise in RViz2:
    ros2 run rviz2 rviz2
    → Add TF display, Fixed Frame = "world"
"""

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TransformStamped, Quaternion
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32

from tf2_ros import TransformBroadcaster


# ─── Car geometry constants ────────────────────────────────────────────────────
WHEELBASE   = 2.7   # m  distance front-to-rear axle
TRACK_WIDTH = 1.6   # m  distance left-to-right wheel centre
WHEEL_RADIUS = 0.35  # m
WHEEL_OFFSET_Z = WHEEL_RADIUS  # wheels sit on the ground, body above

# ─── Motion parameters ─────────────────────────────────────────────────────────
CIRCLE_RADIUS = 8.0   # m   radius of the circular path
LINEAR_SPEED  = 3.0   # m/s car speed along the circle

# Angular speed around the circle: ω = v / r
ANGULAR_SPEED = LINEAR_SPEED / CIRCLE_RADIUS   # rad/s


def euler_to_quaternion(roll: float, pitch: float, yaw: float) -> Quaternion:
    """Convert Euler angles (radians) to a geometry_msgs/Quaternion."""
    cy, sy = math.cos(yaw * 0.5),   math.sin(yaw * 0.5)
    cp, sp = math.cos(pitch * 0.5), math.sin(pitch * 0.5)
    cr, sr = math.cos(roll * 0.5),  math.sin(roll * 0.5)

    q = Quaternion()
    q.w = cr * cp * cy + sr * sp * sy
    q.x = sr * cp * cy - cr * sp * sy
    q.y = cr * sp * cy + sr * cp * sy
    q.z = cr * cp * sy - sr * sp * cy
    return q


class CarTFBroadcaster(Node):
    """
    Broadcasts the TF tree for a car driving in a circle.

    Frame layout
    ────────────
    world        – static, inertial origin
    base_link    – car body centre (ground level, centre of rear axle)
    front_left_wheel  )
    front_right_wheel ) – relative to base_link
    rear_left_wheel   )
    rear_right_wheel  )
    """

    def __init__(self):
        super().__init__('car_tf_broadcaster')

        # ── TF broadcaster ──────────────────────────────────────────────────
        self.tf_broadcaster = TransformBroadcaster(self)

        # ── Publishers ──────────────────────────────────────────────────────
        self.odom_pub    = self.create_publisher(Odometry, 'odom', 10)
        self.speed_pub   = self.create_publisher(Float32, 'car/speed', 10)
        self.heading_pub = self.create_publisher(Float32, 'car/heading_deg', 10)

        # ── State ───────────────────────────────────────────────────────────
        self.t = 0.0          # simulation time [s]
        self.wheel_angle = 0.0  # rolling angle of wheels [rad]

        # ── Timer: 50 Hz update ─────────────────────────────────────────────
        self.dt = 0.02
        self.timer = self.create_timer(self.dt, self.update)

        self.get_logger().info(
            f'Car TF broadcaster started. '
            f'Circle radius={CIRCLE_RADIUS} m, speed={LINEAR_SPEED} m/s'
        )

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _make_transform(self,
                        frame_id: str,
                        child_frame_id: str,
                        tx: float, ty: float, tz: float,
                        roll: float = 0.0,
                        pitch: float = 0.0,
                        yaw: float = 0.0) -> TransformStamped:
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = frame_id
        t.child_frame_id  = child_frame_id
        t.transform.translation.x = tx
        t.transform.translation.y = ty
        t.transform.translation.z = tz
        t.transform.rotation = euler_to_quaternion(roll, pitch, yaw)
        return t

    # ── Main update callback ───────────────────────────────────────────────────

    def update(self):
        self.t += self.dt

        # ── 1. Car pose in world frame ──────────────────────────────────────
        #   Position on circle: x = R·cos(ω·t),  y = R·sin(ω·t)
        #   Heading tangent to circle: yaw = ω·t + π/2
        angle    = ANGULAR_SPEED * self.t          # angular position on circle
        car_x    = CIRCLE_RADIUS * math.cos(angle)
        car_y    = CIRCLE_RADIUS * math.sin(angle)
        car_yaw  = angle + math.pi / 2             # tangent direction

        # ── 2. Wheel rolling angle (all wheels same for straight-line approx)
        self.wheel_angle += LINEAR_SPEED * self.dt / WHEEL_RADIUS
        wheel_pitch = self.wheel_angle             # pitch = rolling

        # ── 3. Broadcast world → base_link ─────────────────────────────────
        tf_car = self._make_transform(
            'world', 'base_link',
            car_x, car_y, WHEEL_RADIUS,   # body centre at wheel-radius height
            yaw=car_yaw
        )
        self.tf_broadcaster.sendTransform(tf_car)

        # ── 4. Broadcast base_link → wheels ────────────────────────────────
        #   Wheel positions relative to base_link (rear-axle centre):
        #     front_*  →  +x = WHEELBASE/2  (forward)
        #     rear_*   →  -x = WHEELBASE/2  (backward)
        #     left_*   →  +y = TRACK_WIDTH/2
        #     right_*  →  -y = TRACK_WIDTH/2
        #   All wheels drop to z=0 (ground) relative to body height
        wheel_z = -WHEEL_RADIUS  # relative to base_link (body is at WHEEL_RADIUS)

        wheel_configs = [
            ('front_left_wheel',   WHEELBASE / 2,   TRACK_WIDTH / 2,  wheel_z),
            ('front_right_wheel',  WHEELBASE / 2,  -TRACK_WIDTH / 2,  wheel_z),
            ('rear_left_wheel',   -WHEELBASE / 2,   TRACK_WIDTH / 2,  wheel_z),
            ('rear_right_wheel',  -WHEELBASE / 2,  -TRACK_WIDTH / 2,  wheel_z),
        ]

        for name, wx, wy, wz in wheel_configs:
            tf_wheel = self._make_transform(
                'base_link', name,
                wx, wy, wz,
                pitch=wheel_pitch   # rolling animation
            )
            self.tf_broadcaster.sendTransform(tf_wheel)

        # ── 5. Publish Odometry ─────────────────────────────────────────────
        odom = Odometry()
        odom.header.stamp    = self.get_clock().now().to_msg()
        odom.header.frame_id = 'world'
        odom.child_frame_id  = 'base_link'

        odom.pose.pose.position.x  = car_x
        odom.pose.pose.position.y  = car_y
        odom.pose.pose.position.z  = WHEEL_RADIUS
        odom.pose.pose.orientation = euler_to_quaternion(0.0, 0.0, car_yaw)

        # Velocity in body frame: purely forward (local +x)
        odom.twist.twist.linear.x  = LINEAR_SPEED
        odom.twist.twist.angular.z = ANGULAR_SPEED

        self.odom_pub.publish(odom)

        # ── 6. Publish telemetry ────────────────────────────────────────────
        speed_msg = Float32()
        speed_msg.data = LINEAR_SPEED
        self.speed_pub.publish(speed_msg)

        heading_msg = Float32()
        heading_msg.data = math.degrees(car_yaw) % 360.0
        self.heading_pub.publish(heading_msg)

        # ── 7. Periodic console log (every ~2 s) ───────────────────────────
        if int(self.t * 10) % 20 == 0:
            self.get_logger().info(
                f't={self.t:.1f}s | '
                f'pos=({car_x:.2f}, {car_y:.2f}) | '
                f'yaw={math.degrees(car_yaw):.1f}°'
            )


def main(args=None):
    rclpy.init(args=args)
    node = CarTFBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Car TF broadcaster shutting down.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
