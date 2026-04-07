from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ros2_tf_car_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='ROS2 TF demo simulating a car moving in a circle with wheel transforms',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'car_tf_broadcaster = ros2_tf_car_demo.car_tf_broadcaster:main',
            'car_tf_listener = ros2_tf_car_demo.car_tf_listener:main',
        ],
    },
)
