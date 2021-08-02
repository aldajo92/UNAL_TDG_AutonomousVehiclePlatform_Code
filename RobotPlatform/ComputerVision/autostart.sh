#!/bin/bash

# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"

VISION_OPENCV=/python3_ws/src/vision_opencv
if !([ -d "$VISION_OPENCV" ]); then
    git clone https://github.com/ros-perception/vision_opencv.git $VISION_OPENCV
    cd /python3_ws/src/vision_opencv && git checkout 1.13.0
    # chmod 777 /python3_ws/src/vision_opencv/cv_bridge/CMakeLists.txt
fi

INSTALL_FOLDER=/python3_ws/install
if !([ -d "$INSTALL_FOLDER" ]); then
    cd /python3_ws \
        && catkin clean --y \
        && catkin init \
        && catkin config --install -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/aarch64-linux-gnu/libpython3.6m.so -DBOOST_ROOT=/usr/include/boost/
        # && catkin config --install

    # Build
    cd /python3_ws/ && catkin build cv_bridge
fi

# Extend environment with new package
source /catkin_ws/devel/setup.bash
source /python3_ws/install/setup.bash --extend

cd /catkin_ws/ && catkin_make

# source /catkin_ws/devel/setup.bash
# source /python3_ws/devel/setup.bash
roslaunch ros_hello_world launcher.launch