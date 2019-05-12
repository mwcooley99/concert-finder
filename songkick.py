import requests
from sqlalchemy_declarative import Artist, get_engine, get_session


def get_search_base_url(search_for):
    return f'https://api.songkick.com/api/3.0/search/{search_for}.json'


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
        session.commit()
    else:
        print(f'{artist.name}\'s songkick_ID is already known')
    break

# Find all of the events for the artists for the upcoming month
# Need to store the venues in the DB first, then the event, since the event
# has a venue id for a foreign key
for artist in session.query(Artist).all():

