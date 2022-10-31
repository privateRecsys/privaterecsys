#!/bin/sh

echo '--- run yarn install'
yarn install

echo '--- run bundle install'
bundle install

# HERE YOU CAN RUN ANY OTHER SCRIPT BEFORE CONTAINER BUILDING

echo '--- create docker image and up it'
sudo docker-compose up -d --build

