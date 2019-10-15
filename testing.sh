#!/bin/sh
set -e # stop on error
pip install --user fake-useragent beautifulsoup4 python-dateutil pytz archiveis pyopenssl
./venues.py
