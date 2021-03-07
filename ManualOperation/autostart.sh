#!/bin/bash

source /catkin_ws/devel/setup.bash
cd /catkin_ws/ && catkin_make
source /catkin_ws/devel/setup.sh
roslaunch motors motors.launch