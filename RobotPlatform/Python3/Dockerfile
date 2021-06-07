FROM ros_base
# install ros tutorials packages
RUN apt-get update && apt-get install -y \
    tmux \
    ros-melodic-image-view \
    && echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc

RUN apt-get install -y python-catkin-tools python3-dev python3-catkin-pkg-modules python3-numpy python3-yaml ros-melodic-cv-bridge

#catkin init
# https://answers.ros.org/question/358223/using-keras-and-cv_bridge-in-ros-melodic/
# https://stackoverflow.com/questions/49221565/unable-to-use-cv-bridge-with-ros-kinetic-and-python3/50291787#50291787
# catkin config -DPYTHON_EXECUTABLE=/usr/bin/python3 -DPYTHON_INCLUDE_DIR=/usr/include/python3.6m -DPYTHON_LIBRARY=/usr/lib/aarch64-linux-gnu/libpython3.6m.so
# catkin config --install

RUN apt-get install python3-pip python3-yaml

# COPY ./autostart.sh /
# RUN chmod +x /autostart.sh
# ENTRYPOINT /autostart.sh
ENTRYPOINT /bin/bash