FROM ros:melodic-ros-base

RUN apt-get update && apt-get install -y \
    tmux wget curl

# Taken from: 
# https://www.geeksforgeeks.org/installation-of-node-js-on-linux/
# https://askubuntu.com/questions/720784/how-to-install-latest-node-inside-a-docker-container
RUN apt-get update && apt-get -y upgrade
RUN curl -sL https://deb.nodesource.com/setup_14.x  | bash -
RUN apt-get -y install nodejs
RUN npm install -g nodemon

COPY ./autostart.sh /
RUN chmod +x /autostart.sh
ENTRYPOINT /autostart.sh

# CMD ["bash"]