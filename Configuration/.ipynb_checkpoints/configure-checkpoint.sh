#!bin/bash

sudo cp jupyter.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/jupyter.service

sudo systemctl daemon-reload

sudo systemctl start jupyter.service
sudo systemctl enable jupyter.service