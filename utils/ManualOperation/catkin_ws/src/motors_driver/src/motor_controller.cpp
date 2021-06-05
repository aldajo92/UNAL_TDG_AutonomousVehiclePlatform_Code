#include "ros/ros.h"
#include "std_msgs/Int32MultiArray.h"
#include <sstream>
#include <geometry_msgs/Twist.h>

class MotorController
{
    public:
        MotorController();
    private:
        void controllerCallback(const sensor_msgs::Joy::ConstPtr& joy);

        ros::NodeHandle node_;
        ros::Publisher motor_pub_;
        ros::Subscriber twist_sub_;

        std_msgs::Int32MultiArray msg;
}

MotorController::MotorController()
{
    ros::NodeHandle node_;
    motor_pub_ = node_.advertise<std_msgs::Int32MultiArray>("command", 100);
    twist_sub_ = node_.subscribe<geometry_msgs::Twist>("motors/motor_twist", 100, &MotorController::controllerCallback, this);

    msg = std_msgs::Int32MultiArray();
    msg.layout.dim.push_back(std_msgs::MultiArrayDimension());
    msg.layout.dim[0].label = "command";
    msg.layout.dim[0].size = 16;
    msg.layout.dim[0].stride = 16;
}

void PS4ControllerMotor::controllerCallback(const geometry_msgs::Twist::ConstPtr& twist)
{
    // geometry_msgs::Twist twist;
    // twist.linear.x = 10*joy->axes[1];
    // twist.angular.z = 10*joy->axes[2];
    // motor_pub_.publish(twist);

    // ROS_INFO("X: [%f], Y: [%f]", joy->axes[1], joy->axes[2]);
    // ROS_INFO("X: [%f], Y: [%f]", twist.linear.x, twist.angular.z);
    msg.data = std::vector<int>{count, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
    // ROS_INFO("[Talker] I published %d\n", count);
    // chatter_publisher.publish(msg);
}

int main(int argc, char **argv){
	ros::init(argc, argv, "motor_controller");
    
    MotorController motor_controller;
    ros::spin();
    
    return 0;
}