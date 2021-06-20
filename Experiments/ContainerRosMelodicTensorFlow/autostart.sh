#!/bin/bash

# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"

cd /python3_ws \
    && catkin init \
    && catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3.6 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/aarch64-linux-gnu/libpython3.6m.so \
    && catkin config --install

# Build
cd /python3_ws/ && catkin build cv_bridge
# Extend environment with new package
source install/setup.bash --extend

cd /catkin_ws/ && catkin_make
source /catkin_ws/devel/setup.bash
roslaunch ros_hello_world launcher.launch