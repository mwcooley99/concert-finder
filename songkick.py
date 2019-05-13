import requests
from sqlalchemy_declarative import Artist, Event, Venue, get_engine, get_session
from datetime import datetime
import test_values


def get_search_base_url(search_for):
    return f'https://api.songkick.com/api/3.0/search/{search_for}.json'


def get_songkick_artist_id(result):
    artist = result['resultsPage']

    return results['resultsPage']['results']['artist']['id']


def make_event(result):
    event_dict = {
        'id': result['id'],
        'date':  datetime.strptime(result['start']['date'], '%Y-%m-%d'),
        'songkick_artist_id':  result['performance'][0]['artist']['id'],
        'venue_id': result['venue']['id']
    }

    return Event(**event_dict)

def make_venue(result):
    venue_dict = {
        'id': result['venue']['id'],
        'name': result['venue']['displayName'],
        'city': result['location']['city']
    }

    return Venue(**venue_dict)

session = get_session()

# Loop through the Artists and find them in songkick
url = get_search_base_url('artists')
params = {
    'apikey': '12345',
    'query': 'The Beatles'
}
for artist in session.query(Artist).all():
    if artist.songkick_id is None:
        params['query'] = artist.name
        results = requests.get(url, params=params)
        print(results.url)
        # Need to add check if it returned anything
        # artist.songkick_id = results['resultsPage']['results']['artist']['id']
        # session.commit()
    else:
        print(f'{artist.name}\'s songkick_ID is already known')
    break

# Find all of the events for the artists for the upcoming month
# Need to store the venues in the DB first, then the event, since the event
# has a venue id for a foreign key
# url = f'https://api.songkick.com/api/3.0/artists/{artist_id}/calendar.json
# for artist in session.query(Artist).all():

# Verifies that the make_event method words
result = test_values.results
print(make_event(result['resultsPage']['results']['event'][0]))
print(make_venue(result['resultsPage']['results']['event'][0]))
