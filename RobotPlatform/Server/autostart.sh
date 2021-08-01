#!/bin/bash

# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"

# cd /catkin_ws/ && catkin_make
# source /catkin_ws/devel/setup.bash
# roslaunch ros_hello_world launcher.launch

cd /nodejs_ros_server/ && npm install && nodemon index.js