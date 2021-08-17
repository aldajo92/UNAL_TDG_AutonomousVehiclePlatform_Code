FROM ros:melodic-ros-base

# install ros tutorials packages
RUN apt-get update && apt-get install -y \
    python-pip \
    tmux \
    && python -m pip install pyserial \
    && echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc

COPY ./autostart.sh /
RUN chmod +x /autostart.sh
ENTRYPOINT /autostart.sh
# ENTRYPOINT /bin/bash