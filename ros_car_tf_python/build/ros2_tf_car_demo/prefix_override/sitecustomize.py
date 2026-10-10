import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/xuelin/repo/robotics/ros_car_tf_python/install/ros2_tf_car_demo'
