#!/bin/sh
set -e # stop on error
pip install --user fake-useragent beautifulsoup4 python-dateutil pytz
#curl -v -L 'https://archive.today/2019-10-15/https://www.slimspresents.com/event-listing/'
./venues.py
#archiveis https://starlinesocialclub.com/event/yip-deceiver
