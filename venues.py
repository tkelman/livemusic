#!/usr/bin/env python
import archiveis
from bs4 import BeautifulSoup
import dateutil.parser
from datetime import datetime, timedelta, date
import pytz
from fake_useragent import UserAgent
import requests


def archived_date(url):
    response = archiveis.api.do_post(url, anyway=0)
    response.raise_for_status()
    doc = BeautifulSoup(response.text, 'html.parser')
    pubdates = doc.find_all(itemprop='pubdate')
    assert len(pubdates) <= 1
    if len(pubdates) == 0:
        return archiveis.api.parse_memento(response)
    return dateutil.parser.isoparse(pubdates[0].attrs['datetime'])


def rearchive_if_older_than(url, threshold_date):
    pubdate = archived_date(url)
    if isinstance(pubdate, datetime):
        age = datetime.now(tz=pytz.utc) - pubdate
        print('{} archived {} ago'.format(url, age))
        if pubdate < threshold_date:
            print('submitted new archive: {}'.format(archiveis.capture(url)))
    else:
        print('{} not yet archived'.format(url))
        print('submitted new archive: {}'.format(pubdate))


def archive_once(url):
    rearchive_if_older_than(url, datetime(1, 1, 1, tzinfo=pytz.utc))


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
    'http://montalvoarts.org/events/',
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
    'https://palaceoffinearts.org/',
    'https://palaceoffinearts.org/events/',
    'https://catalystclub.com/',
    'https://www.holydiversac.com/',
    'http://www.aceofspadessac.com',
]


ua_header = {'User-Agent': UserAgent().chrome}
redirect_prefix = 'https://via.hypothes.is/'


def archive_events(venue_listing_url, event_prefix, venue_top_url='', redirect_only=False):
    # venue_top_url only needed if event links are relative
    response = requests.get(venue_listing_url, headers=ua_header)
    response.raise_for_status()
    doc = BeautifulSoup(response.text, 'html.parser')
    all_events = [link.get('href') for link in doc.find_all('a')
        if link.get('href', '').startswith(event_prefix)]
    for event in set(all_events): # remove duplicates
        if '?' in event:
            event = event[:event.find('?')]
        if not redirect_only:
            archive_once(venue_top_url + event)
        archive_once(redirect_prefix + venue_top_url + event)


if __name__ == '__main__':
    for venue_url in venue_list:
        rearchive_if_older_than(venue_url, datetime.now(tz=pytz.utc) - timedelta(days=2))

    for venue_url in venue_list:
        rearchive_if_older_than(redirect_prefix + venue_url, datetime.now(tz=pytz.utc) - timedelta(days=2))

    this_year = str(date.today().year)
    this_month = str(date.today().month)
    for venue_url in venue_list:
        if venue_url == '':
            assert False
        elif venue_url == 'https://www.rickshawstop.com/':
            archive_events(venue_url, '/e/', venue_url.replace('.com/', '.com'))
        elif venue_url == 'https://www.dnalounge.com/calendar/latest.html':
            archive_events(venue_url, this_month, venue_url.replace('latest.html', this_year + '/'))
        elif venue_url == 'https://www.thefreight.org/shows/':
            archive_events(venue_url, '/event/', venue_url.replace('/shows/', ''))
        elif venue_url == 'https://www.brickandmortarmusic.com/':
            archive_events(venue_url, 'https://www.ticketweb.com/event/', redirect_only=True)
        #elif venue_url == 'https://publicsf.com/calendar':
        #    archive_events(venue_url, )
        #elif venue_url == 'https://oaklandoctopus.org/calendar':
        #    archive_events(venue_url, )
        elif venue_url == 'https://www.riotheatre.com/events':
            archive_events(venue_url, '/events-2/', venue_url.replace('/events', ''))
        elif venue_url == 'https://centerfornewmusic.com/calendar/':
            archive_events(venue_url, venue_url)
        elif venue_url == 'https://lutherburbankcenter.org/events/':
            archive_events(venue_url, venue_url.replace('/events/', '/event/'))
        elif venue_url == 'https://jubjubsthirstparlor.com/events/':
            archive_events(venue_url, venue_url.replace('/events/', '/event/'))
        elif venue_url == 'http://www.adobebooks.com/events':
            archive_events(venue_url, '/events/', venue_url.replace('/events', ''))
        elif venue_url.startswith('http://montalvoarts.org/'):
            archive_events(venue_url, '/exhibitions/', 'http://montalvoarts.org')
            archive_events(venue_url, '/classes/', 'http://montalvoarts.org')
            archive_events(venue_url, '/events/', 'http://montalvoarts.org')
        elif venue_url == 'http://www.uptowntheatrenapa.com/events/':
            archive_events(venue_url, venue_url.replace('/events/', '/event/'))
        elif venue_url == 'https://mezzaninesf.com/events/':
            archive_events(venue_url, venue_url)
        elif venue_url == 'https://renobrewhouse.com/events/':
            archive_events(venue_url, venue_url.replace('/events/', '/event/'))
        elif venue_url == 'https://www.jmaxproductions.net/calendar/':
            archive_events(venue_url, venue_url.replace('/calendar/', '/event/'))
        elif venue_url == 'http://billgrahamcivic.com/event-listing/':
            archive_events(venue_url, venue_url.replace('/event-listing/', '/events/'))
        elif venue_url == 'https://www.neckofthewoodssf.com/calendar/':
            archive_events(venue_url, '/e/', venue_url.replace('/calendar/', ''))


    # TEMPORARY
    archive_once(redirect_prefix + 'https://www.neckofthewoodssf.com/e/karaoke-night-66763035035/')
    archive_once(redirect_prefix + 'https://www.yoshis.com/e/count-basie-orchestra-66619949061/')
    archive_once(redirect_prefix + 'https://www.yoshis.com/e/count-basie-orchestra-66619949061/#')
    archive_once(redirect_prefix + 'https://www.yoshis.com/e/damien-escobar-66619973133/')
    archive_once(redirect_prefix + 'https://www.yoshis.com/e/damien-escobar-66619973133/#')
    archive_once(redirect_prefix + 'https://www.cornerstoneberkeley.com/e/afrocomiccon-73340422177/')
    archive_once(redirect_prefix + 'https://thefillmore.com/event/city-and-colour/')
    archive_once(redirect_prefix + 'https://www.slimspresents.com/e/injury-reserve-69659073163/')
    archive_once(redirect_prefix + 'https://www.slimspresents.com/e/shintaro-sakamoto-sold-out--62092013885/')
    archive_once(redirect_prefix + 'https://www.thechapelsf.com/e/jesse-malin-joseph-arthur-66965115463/')
    archive_once(redirect_prefix + 'https://www.augusthallsf.com/event/9814505/finneas-blood-harmony-tour-2019/')
    archive_once(redirect_prefix + 'https://www.theindependentsf.com/event/9940555/temples/')
    #archive_once('')
    threshold = datetime(2019, 10, 15, 22, tzinfo=pytz.utc)
    rearchive_if_older_than('https://www.thechapelsf.com/e/w-i-t-c-h-we-intend-to-cause-havoc--69227614659/', threshold)
    rearchive_if_older_than('https://www.slimspresents.com/e/fink-61850136423/', threshold)
    rearchive_if_older_than('https://www.slimspresents.com/e/senses-fail-69658102259/', threshold)
    rearchive_if_older_than('https://thefillmore.com/event/the-japanese-house/', threshold)
    rearchive_if_older_than('https://live.stanford.edu/calendar/october-2019/bob-dylan-and-his-band', threshold)
    rearchive_if_older_than('https://www.rickshawstop.com/e/monster-rally-with-mejiwahn-and-lake-cube-69941694491/', threshold)
    rearchive_if_older_than('https://jubjubsthirstparlor.com/event/dreadful-children-lincoln-skinz/', threshold)
    #rearchive_if_older_than('', threshold)
