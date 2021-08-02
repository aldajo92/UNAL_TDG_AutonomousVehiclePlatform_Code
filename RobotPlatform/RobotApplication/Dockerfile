FROM ros:melodic-ros-base

# install ros tutorials packages
RUN apt-get update && apt-get install -y \
    tmux \
    ros-melodic-image-view \
    ros-melodic-tf \
    && echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc

COPY ./autostart.sh /
RUN chmod +x /autostart.sh
ENTRYPOINT /autostart.sh
# ENTRYPOINT /bin/bash