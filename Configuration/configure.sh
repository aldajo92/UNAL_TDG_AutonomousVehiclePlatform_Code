#!bin/bash

sudo systemctl stop jupyter.service
sudo systemctl disable jupyter.service

sudo rm -rf /etc/systemd/system/jupyter.service
sudo cp jupyter.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/jupyter.service

sudo systemctl daemon-reload

sudo systemctl start jupyter.service
sudo systemctl enable jupyter.service
