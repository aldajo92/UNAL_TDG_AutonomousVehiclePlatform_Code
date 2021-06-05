FROM ros:melodic-ros-base

RUN apt-get update && apt-get install -y \
    tmux wget

COPY ./autostart.sh /
RUN chmod +x /autostart.sh
ENTRYPOINT /autostart.sh