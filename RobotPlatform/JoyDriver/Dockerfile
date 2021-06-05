FROM ros_base
# install ros tutorials packages
RUN apt-get update && apt-get install -y \
    tmux \
    && echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc \
    && sudo apt-get install -y ros-melodic-joy

COPY ./autostart.sh /
RUN chmod +x /autostart.sh
ENTRYPOINT /autostart.sh
# ENTRYPOINT /bin/bash