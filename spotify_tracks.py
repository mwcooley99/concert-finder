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


username = os.environ['USERNAME']
token = get_token(username)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_tracks(limit=50, time_range='long_term')

    for k, v in results['items'][0].items():
        print(k, v)

else:
    print("Can't get token for", username)
