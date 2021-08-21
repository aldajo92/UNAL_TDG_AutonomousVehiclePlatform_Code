# # This is an auto generated Dockerfile for ros:ros-core
# # generated from docker_images/create_ros_core_image.Dockerfile.em
# FROM ubuntu:bionic

# # setup timezone
# RUN echo 'Etc/UTC' > /etc/timezone && \
#     ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
#     apt-get update && \
#     apt-get install -q -y --no-install-recommends tzdata && \
#     rm -rf /var/lib/apt/lists/*

# # install packages
# RUN apt-get update && apt-get install -q -y --no-install-recommends \
#     dirmngr \
#     gnupg2 \
#     && rm -rf /var/lib/apt/lists/*

# # setup keys
# RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# # setup sources.list
# RUN echo "deb http://packages.ros.org/ros/ubuntu bionic main" > /etc/apt/sources.list.d/ros1-latest.list

# # setup environment
# ENV LANG C.UTF-8
# ENV LC_ALL C.UTF-8

# ENV ROS_DISTRO melodic

# # install ros packages
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     ros-melodic-ros-core=1.4.1-0* \
#     && rm -rf /var/lib/apt/lists/*

# # install bootstrap tools
# RUN apt-get update && apt-get install --no-install-recommends -y \
#     build-essential \
#     python-rosdep \
#     python-rosinstall \
#     python-vcstools \
#     && rm -rf /var/lib/apt/lists/*

# # bootstrap rosdep
# RUN rosdep init && \
#   rosdep update --rosdistro $ROS_DISTRO

# # install ros packages
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     ros-melodic-ros-base=1.4.1-0* \
#     && rm -rf /var/lib/apt/lists/*

# # setup entrypoint
# COPY ./ros_entrypoint.sh /

# ENTRYPOINT ["/ros_entrypoint.sh"]
# # CMD ["bash"]


FROM nvcr.io/nvidia/l4t-tensorflow:r32.5.0-tf2.3-py3

# setup timezone
RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && \
    apt-get install -q -y --no-install-recommends tzdata && \
    rm -rf /var/lib/apt/lists/*

# install packages
RUN apt-get update && apt-get install -q -y --no-install-recommends \
    dirmngr \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu bionic main" > /etc/apt/sources.list.d/ros1-latest.list

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV ROS_DISTRO melodic

# install ros packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-melodic-ros-core=1.4.1-0* \
    && rm -rf /var/lib/apt/lists/*

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    python-rosdep \
    python-rosinstall \
    python-vcstools \
    && rm -rf /var/lib/apt/lists/*

# bootstrap rosdep
RUN rosdep init && \
  rosdep update --rosdistro $ROS_DISTRO

# install ros packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-melodic-ros-base=1.4.1-0* \
    && rm -rf /var/lib/apt/lists/*

# install ros tutorials packages
RUN apt-get update && apt-get install -y \
    tmux \
    git \
    ros-melodic-image-view \
    && echo "source /catkin_ws/devel/setup.bash" >> /root/.bashrc

RUN apt-get install -y python-catkin-tools python3-dev python3-pip python3-catkin-pkg-modules python3-numpy python3-yaml ros-melodic-cv-bridge \
    python3-opencv

# catkin init
# https://answers.ros.org/question/358223/using-keras-and-cv_bridge-in-ros-melodic/
# https://stackoverflow.com/questions/49221565/unable-to-use-cv-bridge-with-ros-kinetic-and-python3/50291787#50291787
# https://medium.com/@beta_b0t/how-to-setup-ros-with-python-3-44a69ca36674

RUN pip3 install rospkg catkin_pkg

# fix based on: https://answers.ros.org/question/344951/could-not-find-the-following-boost-libraries-boost_python3/
RUN cd /usr/lib/aarch64-linux-gnu && sudo ln -s libboost_python3.a libboost_python36.a && sudo ln -s libboost_python3.so libboost_python36.so

COPY ./ros_entrypoint.sh /
RUN chmod +x /ros_entrypoint.sh
ENTRYPOINT ["/ros_entrypoint.sh"]

# ENTRYPOINT /bin/bash