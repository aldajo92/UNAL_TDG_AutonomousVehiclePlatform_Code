#include "ros/ros.h"
#include "std_msgs/Int32MultiArray.h"
#include <sstream>

int main(int argc, char **argv){
    // Initiate new ROS node named "talker"
	ros::init(argc, argv, "motor_talker");
    // Create a node handle: it is reference assigned to a new node
    ros::NodeHandle node;
    // Create a publisher with a topic "chatter" that will send a Int32MultiArray message
    ros::Publisher chatter_publisher = node.advertise<std_msgs::Int32MultiArray>("command", 1000);
    // Rate is a class used to define frequency for a loop. Here we send a message each two seconds.
    ros::Rate loop_rate(0.5); // one message per second
    
    int count = 5000;
    int fordward = 1;
    
    std_msgs::MultiArrayLayout dim = std_msgs::MultiArrayLayout();
    std_msgs::Int32MultiArray msg = std_msgs::Int32MultiArray();
    msg.layout.dim.push_back(std_msgs::MultiArrayDimension());
    msg.layout.dim[0].label = "command";
    msg.layout.dim[0].size = 16;
    msg.layout.dim[0].stride = 16;
    
    while(ros::ok())
    {
        // Create a new String ROS message
        // Message definition in this link http://dos.ros.org/api/std_msg/html/msg/String.html
//         std_msgs::MultiArrayLayout dim = std_msgs::MultiArrayLayout();
//         std_msgs::Int32MultiArray msg = std_msgs::Int32MultiArray();
        
//         dim[0].label = "command";
//         dim[0].size = 16;
//         dim[0].stride = 16;
        
//         msg.layout.push_back(dim);
        
//         msg.layout.dim.push_back(std_msgs::MultiArrayDimension());
//         msg.layout.dim[0].label = "command";
//         msg.layout.dim[0].size = 16;
//         msg.layout.dim[0].stride = 16;
        
        msg.data = std::vector<int>{count, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1};
        
//         msg.dim = 1;
//         msg.data = 
        //Create a string for the data
//         std::stringstream ss;
//         ss << "hello world " << count;
        
//         //assignd the string data to ROS message data field
//         msg.data = ss.str();
        
//         // Print the content of the message in terminal
        ROS_INFO("[Talker] I published %d\n", count);
        
//         //publish the message
        chatter_publisher.publish(msg);
        
        ros::spinOnce(); // Need to call this function often to allw ROS to process incoming messages
        
        loop_rate.sleep();
        
        if(count < 6400){
//             count+=150;
        }
    }
    return 0;
}