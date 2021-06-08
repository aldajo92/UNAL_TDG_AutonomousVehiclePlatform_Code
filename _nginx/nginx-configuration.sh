#!/bin/bash

sudo apt install nginx
sudo cp jupyter.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/jupyter.conf /etc/nginx/sites-enabled/jupyter.conf
nginx -t

