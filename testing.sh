#!/bin/sh
set -e # stop on error
sudo apt-get update
sudo apt-get -y upgrade
pip install --user -r requirements.txt
./venues.py
