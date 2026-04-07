"""
car_tf_listener.py — ROS2 TF2 Listener Demo

Reads the TF tree published by car_tf_broadcaster and:
  • Computes the pose of each wheel in the world frame
  • Computes the distance between front-left and rear-right wheel (diagonal)
  • Prints a live telemetry table to the terminal

This demonstrates:
  • tf2_ros.Buffer + TransformListener setup
  • lookup_transform() to query any frame pair at any time
  • Transforming points across the frame tree

Run with:
    ros2 run ros2_tf_car_demo car_tf_listener
"""

import math

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration

import tf2_ros
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException


WHEEL_FRAMES = [
    'front_left_wheel',
    'front_right_wheel',
    'rear_left_wheel',
    'rear_right_wheel',
]


def quat_to_yaw(q) -> float:
    """Extract yaw (Z rotation) from a quaternion."""
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class CarTFListener(Node):
    """
    Queries the TF tree to extract world-frame poses for the car body
    and all four wheels, then prints a live telemetry table.
    """

    def __init__(self):
        super().__init__('car_tf_listener')

        # ── TF2 buffer + listener ───────────────────────────────────────────
        self.tf_buffer   = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # ── Poll at 2 Hz (readable console output) ──────────────────────────
        self.timer = self.create_timer(0.5, self.print_telemetry)
        self.get_logger().info('Car TF listener started — querying TF tree …')

    def _lookup(self, target: str, source: str):
        """
        Convenience wrapper: lookup transform from source → target in world.
        Returns TransformStamped or None on failure.
        """
        try:
            return self.tf_buffer.lookup_transform(
                target,
                source,
                rclpy.time.Time(),          # "latest available"
                timeout=Duration(seconds=0.1),
            )
        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().warn(f'TF lookup {source}→{target} failed: {e}')
            return None

    def print_telemetry(self):
        # ── Car body in world frame ─────────────────────────────────────────
        car_tf = self._lookup('world', 'base_link')
        if car_tf is None:
            self.get_logger().info('Waiting for TF tree …')
            return

        pos = car_tf.transform.translation
        rot = car_tf.transform.rotation
        yaw = math.degrees(quat_to_yaw(rot))
        speed_r = math.hypot(pos.x, pos.y)   # distance from origin (≈ circle r)

        lines = [
            '',
            '╔══════════════════════════════════════════════════╗',
            '║         ROS2 TF Car Demo — Live Telemetry        ║',
            '╠══════════════════════════════════════════════════╣',
            f'║  Car body  (base_link → world)                   ║',
            f'║    x = {pos.x:+8.3f} m   y = {pos.y:+8.3f} m        ║',
            f'║    z = {pos.z:+8.3f} m   yaw = {yaw:+8.2f} °      ║',
            f'║    dist from origin = {speed_r:6.3f} m               ║',
            '╠══════════════════════════════════════════════════╣',
            '║  Wheels  (wheel → world)                         ║',
        ]

        wheel_positions = {}
        for frame in WHEEL_FRAMES:
            w_tf = self._lookup('world', frame)
            if w_tf is None:
                lines.append(f'║    {frame:<20s}  — no data —          ║')
                continue
            wp = w_tf.transform.translation
            wheel_positions[frame] = wp
            label = frame.replace('_wheel', '').replace('_', ' ').title()
            lines.append(
                f'║    {label:<18s}  ({wp.x:+7.3f}, {wp.y:+7.3f}) m  ║'
            )

        # ── Diagonal distance FL → RR ───────────────────────────────────────
        if 'front_left_wheel' in wheel_positions and 'rear_right_wheel' in wheel_positions:
            fl = wheel_positions['front_left_wheel']
            rr = wheel_positions['rear_right_wheel']
            diag = math.dist((fl.x, fl.y, fl.z), (rr.x, rr.y, rr.z))
            lines += [
                '╠══════════════════════════════════════════════════╣',
                f'║  FL → RR diagonal (world) = {diag:6.3f} m           ║',
            ]

        lines += [
            '╚══════════════════════════════════════════════════╝',
        ]

        self.get_logger().info('\n'.join(lines))


def main(args=None):
    rclpy.init(args=args)
    node = CarTFListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Car TF listener shutting down.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
