#!/usr/bin/env python
import archiveis
from bs4 import BeautifulSoup
import dateutil.parser
from datetime import datetime, timedelta, date
import pytz
from fake_useragent import UserAgent
import asks
import trio
asks.init('trio')


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
    'https://www.theregencyballroom.com/events/all',
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
    'https://live.stanford.edu/calendar',
    'https://www.golden1center.com/events',
    'https://www.chasecenter.com/events',
    'https://www.thewarfieldtheatre.com/events',
    'https://www.thewarfieldtheatre.com/events/all',
    'https://feltonmusichall.com/',
    'https://www.amoeba.com/live-shows',
    'https://www.amoeba.com/live-shows/upcoming/index.html',
    'https://palaceoffinearts.org/',
    'https://palaceoffinearts.org/events/',
    'https://catalystclub.com/',
    'https://www.holydiversac.com/',
    'http://www.aceofspadessac.com',
    'https://sfmasonic.com/calendar/',
    'http://www.sapcenter.com/events/all',
    'http://1015.com/calendar/',
    'http://theritzsanjose.com/',
    'https://www.oaklandmetro.org/',
    'https://sf-eagle.com/events/list',
    'https://bstreettheatre.org/shows/',
    'https://theploughandstars.com/',
    'https://www.thestarryplough.com/events-',
    'https://www.gunbun.com/events/',
    'https://www.mondaviarts.org/events/upcoming-events',
    'https://www.grandsierraresort.com/reno-entertainment/',
]


ua_header = {'User-Agent': UserAgent().chrome}
redirect_prefix = 'https://via.hypothes.is/'


async def archive_events(session, listing_url, event_prefix, top_url='', include_original=True):
    # top_url only needed if event links are relative
    response = await session.get(listing_url, headers=ua_header)
    response.raise_for_status()
    doc = BeautifulSoup(response.text, 'html.parser')
    all_events = [link.get('href') for link in doc.find_all('a')
        if link.get('href', '').startswith(event_prefix)]
    if venue_url not in (
            'https://www.hotelutah.com/calendar/',
            'https://www.yoshis.com/calendar/',
            'https://www.monarchsf.com/',
            'https://www.monarchsf.com/calendar/the-bar-at-monarch/',
            'https://www.moesalley.com/calendar/',
            'https://www.thegreatnorthernsf.com/events/',
            'https://www.rickshawstop.com/',
            'https://www.neckofthewoodssf.com/calendar/',
            'https://www.slimspresents.com/event-listing/',
            'https://www.theuctheatre.org/',
            'https://www.thenewparish.com/calendar/',
            ): # TODO re enable
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
        for venue_url in venue_list:
            nursery.start_soon(rearchive_if_older_than, session,
                venue_url, datetime.now(tz=pytz.utc) - timedelta(days=2))
            nursery.start_soon(rearchive_if_older_than, session,
                redirect_prefix + venue_url, datetime.now(tz=pytz.utc) - timedelta(days=2))

    this_year = str(date.today().year)
    this_month = str(date.today().month)
    day_of_year = date.today().timetuple().tm_yday
    #day_of_month = date.today().day
    hour_of_day = datetime.now(tz=pytz.utc).hour
    for i, venue_url in enumerate(venue_list):
        # for problematic venue pages, only try during one hour per day
        # different hour per venue, different hour per day
        stagger = (hour_of_day == (day_of_year + i) % 24)
        if venue_url == '':
            assert False
        elif venue_url == 'http://www.makeoutroom.com/events':
            await archive_events(session, venue_url, venue_url.replace('http://', '//'), 'http:')
        elif venue_url == 'https://amnesiathebar.com/calendar/list/':
            await archive_events(session, venue_url, venue_url.replace('/list/', '/'))
        elif venue_url == 'https://www.hotelutah.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/calendar/', ''), include_original=stagger)
        elif venue_url == 'https://www.yoshis.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/calendar/', ''), include_original=stagger)
        elif venue_url == 'http://www.milksf.com/':
            await archive_events(session, venue_url, '/shows/', venue_url[:-1])
        elif venue_url == 'http://www.bottomofthehill.com/calendar.html':
            await archive_events(session, venue_url, venue_url.replace('calendar.html', '') + this_year)
        elif venue_url.startswith('https://www.monarchsf.com/'):
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', 'https://www.monarchsf.com', include_original=stagger)
        elif venue_url == 'https://starlinesocialclub.com/calendar/list':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/event/', venue_url.replace('/calendar/list', ''), include_original=stagger)
        elif venue_url == 'http://thedipredding.com/events/':
            await archive_events(session, venue_url, 'https://facebook.com/events/')
        elif venue_url == 'https://www.harlows.com/all-shows/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url.replace('/all-shows/', '/event/'), include_original=stagger)
        elif venue_url == 'https://boomboomroom.com/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url + 'event_listings/', include_original=stagger)
        elif venue_url == 'https://www.moesalley.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/calendar/', ''), include_original=stagger)
        elif venue_url == 'https://www.thegreatnorthernsf.com/events/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/events/', ''), include_original=stagger)
        #elif venue_url == 'https://themidwaysf.com/calendar/':
        #    await archive_events(session, venue_url, ) #TODO
        elif venue_url == 'http://www.uptownnightclub.com/events/':
            await archive_events(session, venue_url, venue_url.replace('/events/', '/event/'))
        elif venue_url == 'http://www.stocktonlive.com/events/':
            await archive_events(session, venue_url, venue_url)
        elif venue_url == 'https://mystictheatre.com/event-calendar':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, 'https://www.eventbrite.com/', include_original=stagger)
        elif venue_url == 'https://thecrepeplace.com/events/':
            await archive_events(session, venue_url, '/events/', venue_url.replace('/events/', ''))
        elif venue_url == 'https://sierranevada.com/events/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url.replace('/events/', '/event/'), include_original=stagger)
        elif venue_url == 'https://empresstheatre.org/events/':
            await archive_events(session, venue_url, venue_url)
        elif venue_url == 'https://www.crestsacramento.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/event/', venue_url.replace('/calendar/', ''), include_original=stagger)
        elif venue_url == 'https://www.hollandreno.org/calendar/list/':
            await archive_events(session, venue_url, venue_url.replace('/calendar/list/', '/event/'))
        elif venue_url == 'https://www.rickshawstop.com/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('.com/', '.com'), include_original=stagger)
        elif venue_url == 'https://www.dnalounge.com/calendar/latest.html':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, this_month, venue_url.replace('latest.html', this_year + '/'), include_original=stagger)
        elif venue_url == 'https://www.thefreight.org/shows/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/event/', venue_url.replace('/shows/', ''), include_original=stagger)
        elif venue_url == 'https://www.brickandmortarmusic.com/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, 'https://www.ticketweb.com/event/', include_original=stagger)
        #elif venue_url == 'https://publicsf.com/calendar':
        #    await archive_events(session, venue_url, ) #TODO
        #elif venue_url == 'https://oaklandoctopus.org/calendar':
        #    await archive_events(session, venue_url, ) # :(
        elif venue_url == 'https://www.riotheatre.com/events':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/events-2/', venue_url.replace('/events', ''), include_original=stagger)
        elif venue_url == 'https://centerfornewmusic.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url, include_original=stagger)
        elif venue_url == 'https://lutherburbankcenter.org/events/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url.replace('/events/', '/event/'), include_original=stagger)
        elif venue_url == 'https://jubjubsthirstparlor.com/events/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url.replace('/events/', '/event/'), include_original=stagger)
        elif venue_url == 'http://www.adobebooks.com/events':
            await archive_events(session, venue_url, '/events/', venue_url.replace('/events', ''))
        elif venue_url.startswith('http://montalvoarts.org/'):
            await archive_events(session, venue_url, '/exhibitions/', 'http://montalvoarts.org')
            await archive_events(session, venue_url, '/classes/', 'http://montalvoarts.org')
            await archive_events(session, venue_url, '/events/', 'http://montalvoarts.org')
        elif venue_url == 'http://www.uptowntheatrenapa.com/events/':
            await archive_events(session, venue_url, venue_url.replace('/events/', '/event/'))
        elif venue_url == 'https://mezzaninesf.com/events/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url, include_original=stagger)
        elif venue_url == 'https://renobrewhouse.com/events/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url.replace('/events/', '/event/'), include_original=stagger)
        #elif venue_url == 'http://www.paramounttheatre.com/schedule.html':
        #    continue # no separate event pages
        elif venue_url == 'https://www.jmaxproductions.net/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url.replace('/calendar/', '/event/'), include_original=stagger)
        elif venue_url == 'http://billgrahamcivic.com/event-listing/':
            await archive_events(session, venue_url, venue_url.replace('/event-listing/', '/events/'))
        elif venue_url == 'https://www.neckofthewoodssf.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/calendar/', ''), include_original=stagger)
        elif venue_url == 'https://www.slimspresents.com/event-listing/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/event-listing/', ''), include_original=stagger)
        elif venue_url == 'https://www.theuctheatre.org/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url[:-1], include_original=stagger)
        elif venue_url == 'https://www.thenewparish.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/calendar/', ''), include_original=stagger)
        elif venue_url == 'https://thegreekberkeley.com/calendar/':
            await archive_events(session, venue_url, venue_url.replace('/calendar/', '/events/').replace('https://', 'http://'))
        elif venue_url == 'https://thefoxoakland.com/listing/':
            await archive_events(session, venue_url, venue_url.replace('/listing/', '/events/').replace('https://', 'http://'))
        elif venue_url == 'http://www.ashkenaz.com/':
            await archive_events(session, venue_url, '/eventcalendar/', venue_url[:-1])
        elif venue_url == 'https://ivyroom.ticketfly.com':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url, include_original=stagger)
        #elif venue_url == 'https://www.theregencyballroom.com/events':
        #    await archive_events(session, venue_url, venue_url + '/detail/')
        elif venue_url == 'https://www.theregencyballroom.com/events/all':
            # TODO google text-only cache
            await archive_events(session, venue_url, venue_url.replace('/all', '/detail/'))
        elif venue_url == 'https://www.augusthallsf.com/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url + 'event/', include_original=stagger)
        elif venue_url == 'https://thefillmore.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url.replace('/calendar/', '/event/'), include_original=stagger)
        elif venue_url == 'https://www.thechapelsf.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/calendar/', ''), include_original=stagger)
        #elif venue_url == 'http://ritespotcafe.net/calendar.php':
        #    continue # no separate event pages
        elif venue_url == 'https://www.theindependentsf.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url.replace('/calendar/', '/event/'), include_original=stagger)
        elif venue_url == 'http://madroneartbar.com/':
            await archive_events(session, venue_url, venue_url + 'event/')
        # this one seems to give empty results a lot of the time
        #elif venue_url == 'http://madroneartbar.com/calendar/':
        #    await archive_events(session, venue_url, venue_url.replace('/calendar/', '/event/').replace('http://', 'https://'))
        elif venue_url == 'http://www.mountainviewamphitheater.com/events/':
            await archive_events(session, venue_url, venue_url)
        elif venue_url == 'https://sanjosetheaters.org/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, venue_url.replace('/calendar/', '/event/'), include_original=stagger)
        elif venue_url == 'https://www.thephoenixtheater.com/calendar/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/calendar/', ''), include_original=stagger)
        elif venue_url == 'http://www.theoaklandarena.com/events':
            await archive_events(session, venue_url, venue_url)
        elif venue_url == 'https://www.cornerstoneberkeley.com/music-venue/cornerstone-events/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/e/', venue_url.replace('/music-venue/cornerstone-events/', ''), include_original=stagger)
        elif venue_url == 'https://www.theeparkside.com/':
            await archive_events(session, venue_url, '/event/', venue_url[:-1])
        elif venue_url == 'http://theknockoutsf.com/events/':
            await archive_events(session, venue_url, venue_url.replace('/events/', '/event/'))
        elif venue_url == 'https://shows.swedishamericanhall.com/':
            await archive_events(session, venue_url, '/event/', venue_url[:-1])
        #elif venue_url == 'http://www.concordamp.com/events/':
        #    await archive_events(session, venue_url, ) # empty for now?
        #elif venue_url == 'https://live.stanford.edu/venues/frost-amphitheater':
        #    await archive_events(session, venue_url, '/calendar/', venue_url.replace('/venues/frost-amphitheater', ''))
        elif venue_url == 'https://live.stanford.edu/calendar':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, '/calendar/', venue_url.replace('/calendar', ''), include_original=stagger)
        elif venue_url == 'https://www.golden1center.com/events':
            await archive_events(session, venue_url, venue_url)
        elif venue_url == 'https://www.chasecenter.com/events':
            await archive_events(session, venue_url, '/events/', venue_url.replace('/events', ''))
            await archive_events(session, venue_url, '/games/', venue_url.replace('/events', ''))
        #elif venue_url == 'https://www.thewarfieldtheatre.com/events':
        #    await archive_events(session, venue_url, venue_url + '/detail/')
        elif venue_url == 'https://www.thewarfieldtheatre.com/events/all':
            # TODO google text-only cache
            await archive_events(session, venue_url, venue_url.replace('/all', '/detail/'))
        elif venue_url == 'https://feltonmusichall.com/':
            stagger and print('trying problematic venue {} this hour'.format(venue_url))
            await archive_events(session, venue_url, 'https://www.eventbrite.com/', include_original=stagger)
        elif venue_url.startswith('https://www.amoeba.com/live-shows'):
            await archive_events(session, venue_url, '/live-shows/', 'https://www.amoeba.com')
        #elif venue_url == 'https://palaceoffinearts.org/':
        #    await archive_events(session, venue_url, '/event/', venue_url[:-1])
        elif venue_url == 'https://palaceoffinearts.org/events/':
            await archive_events(session, venue_url, '/event/', venue_url.replace('/events/', ''))
        elif venue_url == 'https://catalystclub.com/':
            await archive_events(session, venue_url, venue_url + 'eventbrite-events/')
        #elif venue_url == 'https://www.holydiversac.com/':
        #    await archive_events(session, venue_url, ) #TODO
        elif venue_url == 'http://www.aceofspadessac.com':
            # TODO get this reading the whole event list, not just handful at top from thumbnails
            await archive_events(session, venue_url, venue_url)
        #elif venue_url == 'https://sfmasonic.com/calendar/':
        #    await archive_events(session, venue_url, ) #TODO
        elif venue_url == 'http://www.sapcenter.com/events/all':
            await archive_events(session, venue_url, venue_url.replace('/all', '/detail/'))
        elif venue_url == 'http://1015.com/calendar/':
            await archive_events(session, venue_url, venue_url.replace('/calendar/', '/events/'))
        #elif venue_url == 'http://theritzsanjose.com/':
        #    await archive_events(session, venue_url, ) #TODO
        elif venue_url == 'https://www.oaklandmetro.org/':
            await archive_events(session, venue_url, '/event/', venue_url[:-1])
        elif venue_url == 'https://sf-eagle.com/events/list':
            await archive_events(session, venue_url, venue_url.replace('/events/list', '/event/'))
        elif venue_url == 'https://bstreettheatre.org/shows/':
            await archive_events(session, venue_url, venue_url.replace('/shows/', '/show/'))
        #elif venue_url == 'https://theploughandstars.com/':
        #    continue # no separate event pages
        elif venue_url == 'https://www.thestarryplough.com/events-':
            await archive_events(session, venue_url, 'https://www.eventbrite.com/')
        elif venue_url == 'https://www.gunbun.com/events/':
            await archive_events(session, venue_url, venue_url.replace('/events/', '/event/'))
        elif venue_url == 'https://www.mondaviarts.org/events/upcoming-events':
            await archive_events(session, venue_url, '/event/', venue_url.replace('/events/upcoming-events', ''))
        elif venue_url == 'https://www.grandsierraresort.com/reno-entertainment/':
            await archive_events(session, venue_url, venue_url)


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
    #rearchive_if_older_than('', threshold)


if __name__ == '__main__':
    trio.run(main)
