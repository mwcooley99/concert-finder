import spotipy
import spotipy.util as util

from sqlalchemy_declarative import Artist, Track, Album, engine
from sqlalchemy.orm.session import sessionmaker

import os


def make_session(engine):
    Session = sessionmaker(bind=engine)

    return Session()


def get_token(username):
    scope = 'user-top-read'
    credentials = {
        'client_id': os.environ['SPOTIPY_CLIENT_ID'],
        'client_secret': os.environ['SPOTIPY_CLIENT_SECRET'],
        'redirect_uri': os.environ['SPOTIPY_REDIRECT_URI'],
    }

    return util.prompt_for_user_token(username, scope, **credentials)


def clean_track(track):
    '''
    :param track: The spotify track
    :return: List of objects in the form: [Artist, Album, Track]
    '''
    track_artist = track['artists'][0]
    track_album = track['album']

    track_data = [
        Artist(id=track_artist['id'], name=track_artist['name']),
        Album(id=track_album['id'], title=track_album['name'],
              artist_id=track_artist['id']),
        Track(id=track['id'], title=track['name'],
              duration_ms=track['duration_ms'],
              album_id=track_album['id'])
    ]
    return track_data


def commit(track_data, session):
    '''
    Checks the database for existing records and commits new records
    :param track_data: in the form: [Artist, Album, Track]
    :param session: The current SQLAlchemy session
    '''
    for data in track_data:
        data_type = type(data)
        db_check = session.query(data_type).filter_by(id=data.id).first()

        if db_check is None:
            session.add(data)
            session.commit()
        else:
            print(f'{data} is already in the database')


username = os.environ['USERNAME']
token = get_token(username)

if token:
    sp = spotipy.Spotify(auth=token)
    top_tracks = sp.current_user_top_tracks(limit=50, time_range='long_term')

    session = make_session(engine)

    # Commit the artists, albums and tracks to the database
    for track in top_tracks['items']:
        track_data = clean_track(track)
        commit(track_data, session)


else:
    print("Can't get token for", username)
