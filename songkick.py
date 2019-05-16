import requests
from sqlalchemy_declarative import Artist, Event, Venue, get_engine, \
    get_session
from datetime import datetime


import os
import json


def get_search_base_url(search_for):
    return f'https://api.songkick.com/api/3.0/search/{search_for}.json'


def get_events_base_url(artist_id):
    return f'https://api.songkick.com/api/3.0/artists/{artist_id}/calendar.json'


def get_songkick_artist_id(result_data):
    return result_data['resultsPage']['results']['artist'][0]['id']


def make_event(event, songkick_artist_id):
    # Path to event part: ['resutsPage']['results']['event'] <-- list
    event_dict = {
        'id': event['id'],
        'date': datetime.strptime(event['start']['date'], '%Y-%m-%d'),
        'songkick_artist_id': songkick_artist_id,
        'venue_id': event['venue']['id']
    }
    return Event(**event_dict)


def make_venue(event):
    venue_dict = {
        'id': event['venue']['id'],
        'name': event['venue']['displayName'],
        'city': event['location']['city']
    }

    return Venue(**venue_dict)


# TODO - refactor and decompose this
session = get_session()

# Loop through the Artists and find them in songkick
params_artist = {
    'apikey': os.environ['SONGKICK_API_KEY']
}
params_venue = {
    'apikey': os.environ['SONGKICK_API_KEY']
}


for artist in session.query(Artist).all():
    # TODO - decompose
    url = get_search_base_url('artists')
    if artist.songkick_id is None:
        params_artist['query'] = artist.name
        results = requests.get(url, params=params_artist)
        results_data = results.json()

        # Check if it returned an artist
        try:
            artist.songkick_id = get_songkick_artist_id(results_data)
            print(artist.name)
            print(artist.songkick_id)
        except Exception as e:
            print(e)
            continue

        # session.commit()
    else:
        print(f'{artist.name}\'s songkick_ID is already known')

    # Get a result for the calendar
    url = get_events_base_url(artist.songkick_id)
    results = requests.get(url, params=params_venue).json()
    print(json.dumps(results, indent=4))

    # In case no results are returned
    try:
        events = results['resultsPage']['results']['event']
    except Exception as e:
        print(Exception)
        continue

    # Parse and commit the venues and events to the database
    for event in events:
        # pass that result to the makeVenues function
        curr_venue = make_venue(event)
        # print(curr_venue)
        db_check = session.query(Venue).filter_by(id=curr_venue.id).first()
        if db_check is None:
            print(f'Added {curr_venue}')
            session.add(curr_venue)
        else:
            print(f'{curr_venue} already in DB')
        # pass that result to the makeEvents function
        curr_event = make_event(event, artist.songkick_id)
        db_check = session.query(Event).filter_by(id=curr_event.id).first()
        if db_check is None:
            print(f'Added {curr_event}')
            session.add(curr_event)
        else:
            print(f'{curr_event} is already in the db')

        session.commit()



