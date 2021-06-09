#!/bin/bash

echo "installing dpl"
apt-get update -qy
apt-get install -y ruby-dev
gem install dpl
