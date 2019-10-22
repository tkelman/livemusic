#!/usr/bin/env python
import archiveis
from bs4 import BeautifulSoup
import dateutil.parser
from datetime import datetime, date, timedelta
import pytz
from fake_useragent import UserAgent
import trio
import asks


async def archived_date(session, url):
    response = await archiveis.api.do_post(session, url, anyway=0)
    response.raise_for_status()
    doc = BeautifulSoup(response.text, 'html.parser')
    pubdates = doc.find_all(itemprop='pubdate')
    assert len(pubdates) <= 1
    if len(pubdates) == 0:
        return archiveis.api.parse_memento(response)
    return dateutil.parser.isoparse(pubdates[0].attrs['datetime'])


async def rearchive_if_older_than(session, url, threshold_date):
    pubdate = await archived_date(session, url)
    if isinstance(pubdate, datetime):
        age = datetime.now(tz=pytz.utc) - pubdate
        msg = '{} archived {} ago'.format(url, age)
        if pubdate < threshold_date:
            msg += '\nsubmitted new archive: {}'.format(await archiveis.capture(session, url))
    else:
        msg = '{} not yet archived'.format(url)
        msg += '\nsubmitted new archive: {}'.format(pubdate)
    print(msg)


async def archive_once(session, url):
    await rearchive_if_older_than(session, url, datetime(1, 1, 1, tzinfo=pytz.utc))


this_year = str(date.today().year)
this_month = str(date.today().month)
day_of_year = date.today().timetuple().tm_yday
#day_of_month = date.today().day
hour_of_day = datetime.now(tz=pytz.utc).hour

all_venues = []
all_venues.append({'listing_url': 'http://www.makeoutroom.com/events'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('http://', '//')
all_venues[-1]['top_url'] = 'http:'

all_venues.append({'listing_url': 'https://amnesiathebar.com/calendar/list/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/list/', '/')

all_venues.append({'listing_url': 'https://www.hotelutah.com/calendar/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.yoshis.com/calendar/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'http://www.milksf.com/'})
all_venues[-1]['event_prefix'] = '/shows/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'][:-1]

all_venues.append({'listing_url': 'http://www.bottomofthehill.com/calendar.html'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('calendar.html', '') + this_year

all_venues.append({'listing_url': 'https://www.monarchsf.com/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'][:-1]
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.monarchsf.com/calendar/the-bar-at-monarch/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-2]['top_url']
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://starlinesocialclub.com/calendar/list'})
all_venues[-1]['event_prefix'] = '/event/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar/list', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'http://thedipredding.com/events/'})
all_venues[-1]['event_prefix'] = 'https://facebook.com/events/'

all_venues.append({'listing_url': 'https://www.harlows.com/all-shows/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/all-shows/', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://boomboomroom.com/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'] + 'event_listings/'
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.moesalley.com/calendar/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.thegreatnorthernsf.com/events/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/events/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://themidwaysf.com/calendar/'})
#TODO

all_venues.append({'listing_url': 'http://www.uptownnightclub.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/', '/event/')

all_venues.append({'listing_url': 'http://www.stocktonlive.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url']

all_venues.append({'listing_url': 'https://mystictheatre.com/event-calendar'})
all_venues[-1]['event_prefix'] = 'https://www.eventbrite.com/'
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://thecrepeplace.com/events/'})
all_venues[-1]['event_prefix'] = '/events/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/events/', '')

all_venues.append({'listing_url': 'https://sierranevada.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://empresstheatre.org/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url']

all_venues.append({'listing_url': 'https://www.crestsacramento.com/calendar/'})
all_venues[-1]['event_prefix'] = '/event/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.hollandreno.org/calendar/list/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/list/', '/event/')

all_venues.append({'listing_url': 'https://www.rickshawstop.com/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'][:-1]
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.dnalounge.com/calendar/latest.html'})
all_venues[-1]['event_prefix'] = this_month
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('latest.html', this_year + '/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.thefreight.org/shows/'})
all_venues[-1]['event_prefix'] = '/event/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/shows/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.brickandmortarmusic.com/'})
all_venues[-1]['event_prefix'] = 'https://www.ticketweb.com/event/'
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://publicsf.com/calendar'})
#TODO

all_venues.append({'listing_url': 'https://oaklandoctopus.org/calendar'})
# gone but not forgotten :(

all_venues.append({'listing_url': 'https://www.riotheatre.com/events'})
all_venues[-1]['event_prefix'] = '/events-2/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/events', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://centerfornewmusic.com/calendar/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url']
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://lutherburbankcenter.org/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://jubjubsthirstparlor.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'http://www.adobebooks.com/events'})
all_venues[-1]['event_prefix'] = '/events/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/events', '')

all_venues.append({'listing_url': 'http://montalvoarts.org/calendar/'})
all_venues.append({'listing_url': 'http://montalvoarts.org/events/'})
# special cased below due to multiple event prefixes

all_venues.append({'listing_url': 'http://www.uptowntheatrenapa.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/', '/event/')

all_venues.append({'listing_url': 'https://mezzaninesf.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url']
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://renobrewhouse.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'http://www.paramounttheatre.com/schedule.html'})
# no separate event pages

all_venues.append({'listing_url': 'https://www.jmaxproductions.net/calendar/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'http://billgrahamcivic.com/event-listing/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/event-listing/', '/events/')

all_venues.append({'listing_url': 'https://www.neckofthewoodssf.com/calendar/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.slimspresents.com/event-listing/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/event-listing/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.theuctheatre.org/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'][:-1]
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.thenewparish.com/calendar/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://thegreekberkeley.com/calendar/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/', '/events/').replace('https://', 'http://')

all_venues.append({'listing_url': 'https://thefoxoakland.com/listing/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/listing/', '/events/').replace('https://', 'http://')

all_venues.append({'listing_url': 'http://www.ashkenaz.com/'})
all_venues[-1]['event_prefix'] = '/eventcalendar/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'][:-1]

all_venues.append({'listing_url': 'https://ivyroom.ticketfly.com'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url']
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.theregencyballroom.com/events'})
#all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'] + '/detail/'
all_venues.append({'listing_url': 'https://www.theregencyballroom.com/events/all'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/all', '/detail/')
# TODO archive google text-only cache

all_venues.append({'listing_url': 'https://www.augusthallsf.com/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'] + 'event/'
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://thefillmore.com/calendar/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.thechapelsf.com/calendar/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'http://ritespotcafe.net/calendar.php'})
# no separate event pages

all_venues.append({'listing_url': 'https://www.theindependentsf.com/calendar/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'http://madroneartbar.com/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'] + 'event/'
all_venues.append({'listing_url': 'http://madroneartbar.com/calendar/'})
# this one seems to give empty results a lot of the time
#all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/', '/event/').replace('http://', 'https://')

all_venues.append({'listing_url': 'http://www.mountainviewamphitheater.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url']

all_venues.append({'listing_url': 'https://sanjosetheaters.org/calendar/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.thephoenixtheater.com/calendar/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'http://www.theoaklandarena.com/events'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url']

all_venues.append({'listing_url': 'https://www.cornerstoneberkeley.com/music-venue/cornerstone-events/'})
all_venues[-1]['event_prefix'] = '/e/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/music-venue/cornerstone-events/', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.theeparkside.com/'})
all_venues[-1]['event_prefix'] = '/event/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'][:-1]

all_venues.append({'listing_url': 'http://theknockoutsf.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/', '/event/')

all_venues.append({'listing_url': 'https://shows.swedishamericanhall.com/'})
all_venues[-1]['event_prefix'] = '/event/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'][:-1]

all_venues.append({'listing_url': 'http://www.concordamp.com/events/'})
# empty for now?

all_venues.append({'listing_url': 'https://live.stanford.edu/venues/frost-amphitheater'})
#all_venues[-1]['event_prefix'] = '/calendar/'
#all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/venues/frost-amphitheater', '')
all_venues.append({'listing_url': 'https://live.stanford.edu/calendar'})
all_venues[-1]['event_prefix'] = '/calendar/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/calendar', '')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.golden1center.com/events'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url']

all_venues.append({'listing_url': 'https://www.chasecenter.com/events'})
# special cased below due to multiple event prefixes

all_venues.append({'listing_url': 'https://www.thewarfieldtheatre.com/events'})
#all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'] + '/detail/'
all_venues.append({'listing_url': 'https://www.thewarfieldtheatre.com/events/all'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/all', '/detail/')
# TODO archive google text-only cache

all_venues.append({'listing_url': 'https://feltonmusichall.com/'})
all_venues[-1]['event_prefix'] = 'https://www.eventbrite.com/'
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://www.amoeba.com/live-shows'})
all_venues[-1]['event_prefix'] = '/live-shows/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/live-shows', '')

all_venues.append({'listing_url': 'https://www.amoeba.com/live-shows/upcoming/index.html'})
all_venues[-1]['event_prefix'] = '/live-shows/'
all_venues[-1]['top_url'] = 'https://www.amoeba.com'

all_venues.append({'listing_url': 'https://palaceoffinearts.org/'})
#all_venues[-1]['event_prefix'] = '/event/'
#all_venues[-1]['top_url'] = all_venues[-1]['listing_url'][:-1]
all_venues.append({'listing_url': 'https://palaceoffinearts.org/events/'})
all_venues[-1]['event_prefix'] = '/event/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/events/', '')

all_venues.append({'listing_url': 'https://catalystclub.com/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'] + 'eventbrite-events/'

all_venues.append({'listing_url': 'https://www.holydiversac.com/'})
#TODO

all_venues.append({'listing_url': 'http://www.aceofspadessac.com'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url']
# TODO get this reading the whole event list, not just handful at top from thumbnails

all_venues.append({'listing_url': 'https://sfmasonic.com/calendar/'})
#TODO

all_venues.append({'listing_url': 'http://www.sapcenter.com/events/all'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/all', '/detail/')

all_venues.append({'listing_url': 'http://1015.com/calendar/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/', '/events/')

all_venues.append({'listing_url': 'http://theritzsanjose.com/'})
#TODO

all_venues.append({'listing_url': 'https://www.oaklandmetro.org/'})
all_venues[-1]['event_prefix'] = '/event/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'][:-1]

all_venues.append({'listing_url': 'https://sf-eagle.com/events/list'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/list', '/event/')
all_venues[-1]['problematic'] = True

all_venues.append({'listing_url': 'https://bstreettheatre.org/shows/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/shows/', '/show/')

all_venues.append({'listing_url': 'https://theploughandstars.com/'})
# no separate event pages

all_venues.append({'listing_url': 'https://www.thestarryplough.com/events-'})
all_venues[-1]['event_prefix'] = 'https://www.eventbrite.com/'

all_venues.append({'listing_url': 'https://www.gunbun.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/', '/event/')

all_venues.append({'listing_url': 'https://www.mondaviarts.org/events/upcoming-events'})
all_venues[-1]['event_prefix'] = '/event/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/events/upcoming-events', '')

all_venues.append({'listing_url': 'https://www.grandsierraresort.com/reno-entertainment/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url']

all_venues.append({'listing_url': 'http://pspharbor.com/calendar/list/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/list/', '/event/')
all_venues.append({'listing_url': 'http://pspharbor.com/calendar/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/calendar/', '/event/')

all_venues.append({'listing_url': 'http://www.bridgestorage.com/events/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/', '/event/')
all_venues.append({'listing_url': 'http://www.bridgestorage.com/events/month/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'].replace('/events/month/', '/event/')

all_venues.append({'listing_url': 'https://rockstaruniversity.com/'})
all_venues[-1]['event_prefix'] = all_venues[-1]['listing_url'] + 'events/'

all_venues.append({'listing_url': 'http://www.papamurphyspark.com/events/calendar/'})
all_venues[-1]['event_prefix'] = '/event/'
all_venues[-1]['top_url'] = all_venues[-1]['listing_url'].replace('/events/calendar/', '')

# reno events center? tyler the creator 10/17
# pro arts
# eli's
# castro theater
# thrillhouse records
# pianofight
# event center? gryffin 10/19
# bing concert hall
# caravan
# blacksmith square
# winters tavern
# memorial auditorium
# lincoln theater
# mountain winery
# benders
# golden bull
# elbo
# valencia room
# stork club
# gilman


ua_header = {'User-Agent': UserAgent().chrome}
redirect_prefix = 'https://via.hypothes.is/'


async def archive_events(session, listing_url, event_prefix, top_url='', include_original=True):
    # top_url only needed if event links are relative
    response = await session.get(listing_url, headers=ua_header)
#        verify=(listing_url != 'https://ivyroom.ticketfly.com')) # TODO remove this
    response.raise_for_status()
    doc = BeautifulSoup(response.text, 'html.parser')
    all_events = [link.get('href') for link in doc.find_all('a')
        if link.get('href', '').startswith(event_prefix)]
#    if listing_url not in (
#            'https://www.hotelutah.com/calendar/',
#            'https://www.yoshis.com/calendar/',
#            'https://www.monarchsf.com/',
#            'https://www.monarchsf.com/calendar/the-bar-at-monarch/',
#            'https://www.moesalley.com/calendar/',
#            'https://www.thegreatnorthernsf.com/events/',
#            'https://www.rickshawstop.com/',
#            'https://www.neckofthewoodssf.com/calendar/',
#            'https://www.slimspresents.com/event-listing/',
#            'https://www.theuctheatre.org/',
#            'https://www.thenewparish.com/calendar/',
#            'https://ivyroom.ticketfly.com',
#            ):
    assert len(all_events) > 0
    async with trio.open_nursery() as nursery:
        for event in set(all_events): # remove duplicates
            if '?' in event and not event.startswith('http://www.aceofspadessac.com'):
                event = event[:event.find('?')]
            if event == 'http://www.stocktonlive.com/events/rss':
                continue # skip this
            if include_original:
                nursery.start_soon(archive_once, session, top_url + event)
            nursery.start_soon(archive_once, session, redirect_prefix + top_url + event)
            if top_url == 'https://www.yoshis.com':
                if include_original:
                    nursery.start_soon(archive_once, session, top_url + event + '#')
                nursery.start_soon(archive_once, session, redirect_prefix + top_url + event + '#')


session = asks.Session(connections=3)

async def main():
    async with trio.open_nursery() as nursery:
        for venue in all_venues:
            nursery.start_soon(rearchive_if_older_than, session,
                venue['listing_url'], datetime.now(tz=pytz.utc) - timedelta(days=2))
            nursery.start_soon(rearchive_if_older_than, session,
                redirect_prefix + venue['listing_url'], datetime.now(tz=pytz.utc) - timedelta(days=2))

    prob_counter = 0
    for venue in all_venues:
        venue_url = venue['listing_url']
        if venue.get('problematic', False):
            prob_counter += 1
            # for problematic venue pages, only try during one hour per day
            # different hour per venue, different hour per day
            include_original = (hour_of_day == (day_of_year + prob_counter) % 24)
            if include_original:
                print('trying problematic venue {} this hour'.format(venue_url))
        else:
            include_original = True

        if venue_url == '':
            assert False
        elif venue_url.startswith('http://montalvoarts.org/'):
            await archive_events(session, venue_url, '/exhibitions/', 'http://montalvoarts.org')
            await archive_events(session, venue_url, '/classes/', 'http://montalvoarts.org')
            await archive_events(session, venue_url, '/events/', 'http://montalvoarts.org')
        elif venue_url == 'https://www.chasecenter.com/events':
            await archive_events(session, venue_url, '/events/', venue_url.replace('/events', ''))
            await archive_events(session, venue_url, '/games/', venue_url.replace('/events', ''))
        else:
            if 'event_prefix' in venue.keys():
                await archive_events(session, venue_url, venue['event_prefix'],
                    venue.get('top_url', ''), include_original)


    # TEMPORARY
    #archive_once('https://www.neckofthewoodssf.com/e/karaoke-night-66763035035/')
    #archive_once('https://www.yoshis.com/e/count-basie-orchestra-66619949061/')
    #archive_once('https://www.yoshis.com/e/count-basie-orchestra-66619949061/#')
    #archive_once('https://www.yoshis.com/e/damien-escobar-66619973133/')
    #archive_once('https://www.yoshis.com/e/damien-escobar-66619973133/#')
    #archive_once('https://www.cornerstoneberkeley.com/e/afrocomiccon-73340422177/')
    #archive_once('https://thefillmore.com/event/city-and-colour/')
    #archive_once('https://www.slimspresents.com/e/injury-reserve-69659073163/')
    #archive_once('https://www.slimspresents.com/e/shintaro-sakamoto-sold-out--62092013885/')
    #archive_once('https://www.thechapelsf.com/e/jesse-malin-joseph-arthur-66965115463/')
    #archive_once('https://www.augusthallsf.com/event/9814505/finneas-blood-harmony-tour-2019/')
    #archive_once('https://www.theindependentsf.com/event/9940555/temples/')
    #archive_once('')
    #threshold = datetime(2019, 10, 15, 22, tzinfo=pytz.utc)
    #rearchive_if_older_than('https://www.thechapelsf.com/e/w-i-t-c-h-we-intend-to-cause-havoc--69227614659/', threshold)
    #rearchive_if_older_than('https://www.slimspresents.com/e/fink-61850136423/', threshold)
    #rearchive_if_older_than('https://www.slimspresents.com/e/senses-fail-69658102259/', threshold)
    #rearchive_if_older_than('https://thefillmore.com/event/the-japanese-house/', threshold)
    #rearchive_if_older_than('https://live.stanford.edu/calendar/october-2019/bob-dylan-and-his-band', threshold)
    #rearchive_if_older_than('https://www.rickshawstop.com/e/monster-rally-with-mejiwahn-and-lake-cube-69941694491/', threshold)
    #rearchive_if_older_than('https://jubjubsthirstparlor.com/event/dreadful-children-lincoln-skinz/', threshold)
    #rearchive_if_older_than('https://thefillmore.com/event/cautious-clay/', threshold)
    #rearchive_if_older_than('https://www.yoshis.com/e/john-daversa-progressive-big-band-66619951067/', threshold)
    #threshold = datetime(2019, 10, 18, 22, tzinfo=pytz.utc)
    #rearchive_if_older_than('https://lutherburbankcenter.org/event/left-edge-theatre-presents-between-riverside-and-crazy/2019-10-18/', threshold)
    #rearchive_if_older_than('https://www.dnalounge.com/calendar/2019/10-19.html', threshold)
    #threshold = datetime(2019, 10, 20, 14, tzinfo=pytz.utc)
    #rearchive_if_older_than('https://lutherburbankcenter.org/event/left-edge-theatre-presents-between-riverside-and-crazy/2019-10-20/', threshold)
    #rearchive_if_older_than('https://www.monarchsf.com/e/werd-johnnie-walker-smokes-68547805331/', threshold)
    #rearchive_if_older_than('https://www.thenewparish.com/e/hot-brass-band-69350664705/', threshold)
    #rearchive_if_older_than('https://www.thephoenixtheater.com/e/the-rocky-horror-picture-show-72719095773/', threshold)
    #rearchive_if_older_than('https://www.hotelutah.com/e/noah-sheikh-ktl-chris-tewhill-74974802653/', threshold)
    #rearchive_if_older_than('', threshold)


if __name__ == '__main__':
    trio.run(main)
