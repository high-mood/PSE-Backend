from time import sleep
from datetime import datetime
import requests
import sys
# from influxdb import InfluxDBClient

'''
Find recommendations given max 5 song ID's.
The recommendations are based on the given songs
and can be based on additional parameters for the given mood.

Parameters:
tracks    - list of given songs
token - oath token for spotify

Return
List of 5 tuple recommendations consisting of song id,
song name, main artist and playable link.
'''
def get_parameter_string(min_key=0.0, min_mode=0,
                         min_acousticness=0.0, min_danceablility=0.0,
                         min_energy=0.0, min_instrumentalness=0.0,
                         min_liveness=0.0, min_loudness=0.0,
                         min_speechiness=0.0, min_valence=0.0, min_tempo=0.0,
                         max_key=11.0, max_mode=1,
                         max_acousticness=1.0, max_danceablility=1.0,
                         max_energy=1.0, max_instrumentalness=1.0,
                         max_liveness=1.0, max_loudness=1.0,
                         max_speechiness=1.0, max_valence=1.0, max_tempo=1.0):

    return '''&min_key{min_key}&max_key{max_key}
              &min_mode{min_mode}&max_mode{max_mode}
              &min_acousticness{min_acousticness}&max_acousticness{max_acousticness}
              &min_danceablility(min_danceablility}&max_danceablility{max_danceablility}
              &min_energy{min_energy}&max_energy{max_energy}
              &min_instrumentalness{min_instrumentalness}&max_instrumentalness{max_instrumentalness}
              &min_liveness{min_liveness}&max_liveness{max_liveness}
              &min_loudness{min_loudness}&max_loudness{max_loudness}
              &min_speechiness{min_speechiness}&max_speechiness{max_speechiness}
              &min_valence{min_valence}&max_valence{max_valence}
              &min_tempo{min_tempo}&max_tempo{max_tempo}'''

def find_song_recommendations(tracks, token, endpoint="https://api.spotify.com/v1/recommendations"):
    track_string = '%2c'.join(tracks)
    param_string = get_parameter_string()
    r = requests.get(endpoint + "?limit=5&seed_tracks=" + track_string + param_string, headers={"Authorization": "Bearer "+ token})
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        quit()

    song_recommendation = r.json()['tracks']
    recommendations = []
    for i in range(0, 5):
        recommendations.append((song_recommendation[i]['id'], song_recommendation[i]['name'], song_recommendation[i]['artists'][0]['name'], song_recommendation[i]['external_urls']['spotify']))
    return recommendations
