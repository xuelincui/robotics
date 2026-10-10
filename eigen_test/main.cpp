#include <iostream>
#include <Eigen/Dense>
#include <Eigen/Geometry>

int main()
{
    // Define a point in frame A
    Eigen::Vector3d point_A = Eigen::Vector3d::Zero();
    point_A << 1.0, 2.0, 3.0;

    // Define transform from frame A to frame B:
    Eigen::Affine3d T_B_A = Eigen::Affine3d::Identity();
    T_B_A.rotate(Eigen::AngleAxisd(10.0 * M_PI/180.0, Eigen::Vector3d::UnitX()));
    T_B_A.rotate(Eigen::AngleAxisd(20.0 * M_PI/180.0, Eigen::Vector3d::UnitY()));
    T_B_A.rotate(Eigen::AngleAxisd(30.0 * M_PI/180.0, Eigen::Vector3d::UnitZ()));
    T_B_A.translation() = Eigen::Vector3d(1.0, 2.0, 0.0);

    // Transform point from A to B
    Eigen::Vector3d point_B = T_B_A * point_A;

    std::cout << "Point in frame A: " << point_A.transpose() << std::endl;
    std::cout << "Point in frame B: " << point_B.transpose() << std::endl;

    // Inverse transform: go back from B to A
    Eigen::Vector3d point_A_recovered = T_B_A.inverse() * point_B;
    std::cout << "Point recovered in frame A: " << point_A_recovered.transpose() << std::endl;


    return 0;
}
