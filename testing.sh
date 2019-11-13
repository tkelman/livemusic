#!/bin/sh
set -e # stop on error
sudo apt-get install tor
sudo sed -i 's/#ControlPort 9051/ControlPort 9051/' /etc/tor/torrc
sudo service tor start
sudo pip install -r requirements.txt
sudo ./venues.py
