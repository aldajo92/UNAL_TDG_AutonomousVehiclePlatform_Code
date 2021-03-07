#include "ros/ros.h"
#include "std_msgs/Int32MultiArray.h"
#include <sstream>
#include <sensor_msgs/Joy.h>
#include <geometry_msgs/Twist.h>

class PS4ControllerMotor
{
public: 
    PS4ControllerMotor();
    
private:
    void controllerCallback(const sensor_msgs::Joy::ConstPtr& joy);

    ros::NodeHandle node_;
    ros::Publisher motor_pub_;
    ros::Subscriber joy_sub_;
};

PS4ControllerMotor::PS4ControllerMotor()
{
    // creates the publisher
    motor_pub_ = node_.advertise<geometry_msgs::Twist>("motors/motor_twist", 10);

    // creates the subscriber
    joy_sub_ = node_.subscribe<sensor_msgs::Joy>("joy", 100, &PS4ControllerMotor::controllerCallback, this);
}

void PS4ControllerMotor::controllerCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
    geometry_msgs::Twist twist;
    twist.linear.x = joy->axes[1];
    twist.angular.z = joy->axes[2];
    motor_pub_.publish(twist);

    // ROS_INFO("X: [%f], Y: [%f]", joy->axes[1], joy->axes[2]);
    // ROS_INFO("X: [%f], Y: [%f]", twist.linear.x, twist.angular.z);
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "joy_motor");
    PS4ControllerMotor PS4ControllerMotor;
    
    ros::spin();
    return 0;
}