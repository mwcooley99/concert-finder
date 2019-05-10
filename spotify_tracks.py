import spotipy
import spotipy.util as util

import os


def get_token(username):
    scope = 'user-top-read'
    credentials = {
        'client_id': os.environ['SPOTIPY_CLIENT_ID'],
        'client_secret': os.environ['SPOTIPY_CLIENT_SECRET'],
        'redirect_uri': os.environ['SPOTIPY_REDIRECT_URI'],
    }

    return util.prompt_for_user_token(username, scope, **credentials)


def get_artist(track):
    '''
    Takes in a list of tracks and finds the unique artists contained within
    :param tracks: list of track dicts --> format from Spotify API
    :return: List of Artist Classes
    '''

    return None


def clean_track(track):
    '''
    Format the tracks into Track Classes
    :param tracks: list of track dicts --> format from Spotify API
    :return: List of Track Classes
    '''

    return None


def get_album(track):
    '''
    Find all unique albums and turn them into album Classes
    :param tracks: list of track dicts --> format from Spotify API
    :return: List of Album classes
    '''

    return None


username = os.environ['USERNAME']
token = get_token(username)

if token:
    sp = spotipy.Spotify(auth=token)
    top_tracks = sp.current_user_top_tracks(limit=50, time_range='long_term')

    for k, v in top_tracks['items'][0].items():
        print(k, v.keys)

    artists = []
    for track in top_tracks:
        artists.append(get_artist(top_tracks))

else:
    print("Can't get token for", username)
