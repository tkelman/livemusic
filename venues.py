#!/usr/bin/env python
from fake_useragent import UserAgent
import requests
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import dateutil.parser
import pytz


def archived_date(venue_url, redirect=False):
    prefix = ''
    if redirect:
        prefix = 'https://via.hypothes.is/'
    ua = UserAgent()
    ret = requests.get('{}https://archive.today/{}/{}{}'.format(
        prefix, date.today() + timedelta(days=1), prefix, venue_url),
        headers={'User-Agent': ua.chrome})
    ret.raise_for_status()
    doc = BeautifulSoup(ret.text, 'html.parser')
    pubdates = doc.find_all(itemprop='pubdate')
    assert len(pubdates) == 1
    return dateutil.parser.isoparse(pubdates[0].attrs['datetime'])


venue_url = 'https://www.slimspresents.com/event-listing/'
print('{} archived {} ago'.format(venue_url,
    datetime.now(tz=pytz.utc) - archived_date(venue_url)))
#ret = requests.get('https://via.hypothes.is/http://archive.today/20191010/https://www.slimspresents.com/event-listing/')
