#!/bin/sh
set -e # stop on error
pip install --user -r requirements.txt
pip install --user --upgrade requests[security]
./venues.py
