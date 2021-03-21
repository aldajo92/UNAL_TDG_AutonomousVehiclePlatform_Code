#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install curl python3-pip libffi-dev python-openssl libssl-dev zlib1g-dev gcc g++ make -y
curl -sSL https://get.docker.com/ | sh
python3 -m pip install -U pip
sudo pip3 install docker-compose
sudo docker-compose --version