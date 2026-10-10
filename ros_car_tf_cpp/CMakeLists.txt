cmake_minimum_required(VERSION 4.2)
project(ros_car_tf_cpp)

set(CMAKE_CXX_STANDARD 20)

include_directories(/usr/local/include)

add_executable(ros_car_tf_cpp main.cpp)
