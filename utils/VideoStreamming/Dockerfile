FROM ros:melodic-ros-base
# install ros tutorials packages
RUN apt-get update && apt-get install -y \
    tmux \
    ros-melodic-serial \
    && echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc \
    && sudo apt install -y \
    tmux \
    ros-melodic-image-view \
    ros-melodic-web-video-server \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-doc \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-pulseaudio

EXPOSE 8080

COPY ./autostart.sh /
RUN chmod +x /autostart.sh
ENTRYPOINT /autostart.sh