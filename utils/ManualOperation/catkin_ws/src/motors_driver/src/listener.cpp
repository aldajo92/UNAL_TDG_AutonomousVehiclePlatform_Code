#include "ros/ros.sh"
#include "std_msgs/String.h"
#include <sstream>

int main(int argc, char **argv){
    // Initiate new ROS node named "talker"
	ros::init(argc, argv, "listener");
    // Create a node handle: it is reference assigned to a new node
    ros::NodeHandle node;
    // Create a publisher with a topic "chatter" taht will send a String message
    ros::Publisher chatter_publisher = node.advertise<std_msgs::String>("chatter", 1000);
    // Rate is a class used to define frequency for a loop. Here we send a message each two seconds.
    ros::Rate loop_rate(1.0);
    int count = 0;
    
    while(ros::ok())
    {
        // Create a new String ROS message
        // Message definition in this link http://dos.ros.org/api/std_msg/html/msg/String.html
        std_msgs::String msg;
    }

}
