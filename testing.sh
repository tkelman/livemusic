#!/bin/sh
set -e # stop on error
pip install --user -r requirements.txt
./venues.py
