FROM ros:melodic-ros-base
# install ros tutorials packages
RUN apt-get update && apt-get install -y \
    tmux \
    ros-melodic-serial \
    && echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc \
    && sudo apt install -y \
    tmux \
    ros-melodic-image-view \
    ros-melodic-joy \
    python-rosparam

COPY ./autostart.sh /
RUN chmod +x /autostart.sh
ENTRYPOINT /autostart.sh