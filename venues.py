#!/usr/bin/env python
from fake_useragent import UserAgent
import requests
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import dateutil.parser
import pytz
import archiveis


def archived_date(venue_url, redirect=False):
    prefix = ''
    if redirect:
        prefix = 'https://via.hypothes.is/'
    ua = UserAgent()
    ret = requests.get('{}https://archive.today/{}/{}{}'.format(
        prefix, date.today() + timedelta(days=1), prefix, venue_url),
        headers={'User-Agent': ua.chrome})
    if ret.status_code == 404:
        # not yet archived
        return None
    ret.raise_for_status()
    doc = BeautifulSoup(ret.text, 'html.parser')
    pubdates = doc.find_all(itemprop='pubdate')
    assert len(pubdates) == 1
    return dateutil.parser.isoparse(pubdates[0].attrs['datetime'])


venue_list = [
    'http://www.makeoutroom.com/events',
    'https://amnesiathebar.com/calendar/list/',
    'https://www.hotelutah.com/calendar/',
    'https://www.yoshis.com/calendar/',
    'http://www.milksf.com/',
    'http://www.bottomofthehill.com/calendar.html',
    'https://www.monarchsf.com/',
    'https://www.monarchsf.com/calendar/the-bar-at-monarch/',
    'https://starlinesocialclub.com/calendar/list',
    'http://thedipredding.com/events/',
    'https://www.harlows.com/all-shows/',
    'https://boomboomroom.com/',
    'https://www.moesalley.com/calendar/',
    'https://www.thegreatnorthernsf.com/events/',
    'https://themidwaysf.com/calendar/',
    'http://www.uptownnightclub.com/events/',
    'http://www.stocktonlive.com/events/',
    'https://mystictheatre.com/event-calendar',
    'https://thecrepeplace.com/events/',
    'https://sierranevada.com/events/',
    'https://empresstheatre.org/events/',
    'https://www.crestsacramento.com/calendar/',
    'https://www.hollandreno.org/calendar/list/',
    'https://www.rickshawstop.com/',
    'https://www.dnalounge.com/calendar/latest.html',
    'https://www.thefreight.org/shows/',
    'https://www.brickandmortarmusic.com/',
    'https://publicsf.com/calendar',
    'https://oaklandoctopus.org/calendar',
    'https://www.riotheatre.com/events',
    'https://centerfornewmusic.com/calendar/',
    'https://lutherburbankcenter.org/events/',
    'https://jubjubsthirstparlor.com/events/',
    'http://www.adobebooks.com/events',
    'http://montalvoarts.org/calendar/',
    'http://www.uptowntheatrenapa.com/events/',
    'https://mezzaninesf.com/events/',
    'https://renobrewhouse.com/events/',
    'http://paramounttheatre.com/schedule.html',
    'https://www.jmaxproductions.net/calendar/',
    'http://billgrahamcivic.com/event-listing/',
    'https://www.neckofthewoodssf.com/calendar/',
    'https://www.slimspresents.com/event-listing/',
]

for venue_url in venue_list:
    pubdate = archived_date(venue_url)
    if pubdate is None:
        print('{} not yet archived'.format(venue_url))
        archiveis.capture(venue_url)
    else:
        age = datetime.now(tz=pytz.utc) - pubdate
        print('{} archived {} ago'.format(venue_url, age))
        if age > timedelta(days=2):
            archiveis.capture(venue_url)
