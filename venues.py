#!/usr/bin/env python
from fake_useragent import UserAgent
import requests
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import dateutil.parser
import pytz
import archiveis


redirect_prefix = 'https://via.hypothes.is/'


def archived_date(venue_url, redirect=False):
    prefix = ''
    if redirect:
        prefix = redirect_prefix
    ua = UserAgent()
    ret = requests.get('{}https://archive.today/{}/{}'.format(
        prefix, date.today() + timedelta(days=1), venue_url),
        headers={'User-Agent': ua.chrome})
    if ret.status_code == 404:
        # not yet archived
        return None
    ret.raise_for_status()
    doc = BeautifulSoup(ret.text, 'html.parser')
    pubdates = doc.find_all(itemprop='pubdate')
    assert len(pubdates) == 1
    return dateutil.parser.isoparse(pubdates[0].attrs['datetime'])


def rearchive_if_old(venue_url, threshold_days=2):
    pubdate = archived_date(venue_url)
    if pubdate is None:
        print('{} not yet archived'.format(venue_url))
    else:
        age = datetime.now(tz=pytz.utc) - pubdate
        print('{} archived {} ago'.format(venue_url, age))

    if pubdate is None or age > timedelta(days=threshold_days):
        print('submitted new archive: {}'.format(archiveis.capture(venue_url)))


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
    'http://www.paramounttheatre.com/schedule.html',
    'https://www.jmaxproductions.net/calendar/',
    'http://billgrahamcivic.com/event-listing/',
    'https://www.neckofthewoodssf.com/calendar/',
    'https://www.slimspresents.com/event-listing/',
    'https://www.theuctheatre.org/',
    'https://www.thenewparish.com/calendar/',
    'https://thegreekberkeley.com/calendar/',
    'https://thefoxoakland.com/listing/',
    'http://www.ashkenaz.com/',
    'https://ivyroom.ticketfly.com',
    'https://www.theregencyballroom.com/events',
    'https://www.augusthallsf.com/',
    'https://thefillmore.com/calendar/',
    'https://www.thechapelsf.com/calendar/',
    'http://ritespotcafe.net/calendar.php',
    'https://www.theindependentsf.com/calendar/',
    'http://madroneartbar.com/',
    'http://madroneartbar.com/calendar/',
    'http://www.mountainviewamphitheater.com/events/',
    'https://sanjosetheaters.org/calendar/',
    'https://www.thephoenixtheater.com/calendar/',
    'http://www.theoaklandarena.com/events',
    'https://www.cornerstoneberkeley.com/music-venue/cornerstone-events/',
    'https://www.theeparkside.com/',
    'http://theknockoutsf.com/events/',
    'https://shows.swedishamericanhall.com/',
    'http://www.concordamp.com/events/',
    'https://live.stanford.edu/venues/frost-amphitheater',
    'https://www.golden1center.com/events',
    'https://www.chasecenter.com/events',
    'https://www.thewarfieldtheatre.com/events',
    'https://feltonmusichall.com/',
    'https://www.amoeba.com/live-shows',
    'https://www.amoeba.com/live-shows/upcoming/index.html',
]

for venue_url in venue_list:
    rearchive_if_old(venue_url, threshold_days=2)

for venue_url in venue_list:
    rearchive_if_old(redirect_prefix + venue_url, threshold_days=4)
