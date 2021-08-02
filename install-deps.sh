#!/bin/bash

# taken from: 
#   - https://www.digitalocean.com/community/questions/how-to-fix-docker-got-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket
#   - https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-jetson-nano-4gb-2gb-in-2-simple-steps-1f4i

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install curl python3-pip libffi-dev python-openssl libssl-dev zlib1g-dev gcc g++ make nano -y
# curl -sSL https://get.docker.com/ | sh
python3 -m pip install -U pip
sudo pip3 install docker-compose
sudo docker-compose --version

sudo groupadd docker
sudo usermod -aG docker ${USER}
# su -s ${USER}
# docker run hello-world