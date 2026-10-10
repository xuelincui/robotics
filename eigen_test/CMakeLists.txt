cmake_minimum_required(VERSION 4.2)
project(eigen_test)

set(CMAKE_CXX_STANDARD 20)
include_directories(/usr/local/include/eigen-5.0.0)

add_executable(eigen_test main.cpp)
