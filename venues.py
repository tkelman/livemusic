#!/usr/bin/env python
import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup
import dateutil.parser


def archived_date(venue_url, redirect=False):
    prefix = ''
    if redirect:
        prefix = 'https://via.hypothes.is/'
    ret = requests.get('{}https://archive.today/{}/{}'.format(
        prefix, date.today() + timedelta(days=1), venue_url))
    ret.raise_for_status()
    doc = BeautifulSoup(ret.text, 'html.parser')
    pubdates = doc.find_all(itemprop='pubdate')
    assert len(pubdates) == 1
    return dateutil.parser.isoparse(pubdates[0].attrs['datetime'])


print(archived_date('https://www.slimspresents.com/event-listing/'))
#ret = requests.get('https://via.hypothes.is/http://archive.today/20191010/https://www.slimspresents.com/event-listing/')
