#!/bin/bash

source /catkin_ws/devel/setup.bash
cd /catkin_ws/ && catkin_make
source /catkin_ws/devel/setup.sh
roslaunch video_streamming videoStreamming.launch