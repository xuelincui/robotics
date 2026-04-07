import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/xuelin/repo/robotics_sim/install/ros2_tf_car_demo'
