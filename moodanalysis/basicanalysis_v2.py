""" new version of the basic analyser, with weights as parameters in dicts"""

import sys


# Kanye West: I Love It
af1 = {
    "danceability": 0.901,
    "energy": 0.522,
    "key": 2,
    "loudness": -8.304,
    "mode": 1,
    "speechiness": 0.33,
    "acousticness": 0.0114,
    "instrumentalness": 0,
    "liveness": 0.259,
    "valence": 0.329,
    "tempo": 104.053,
    "type": "audio_features",
    "id": "4S8d14HvHb70ImctNgVzQQ",
    "uri": "spotify:track:4S8d14HvHb70ImctNgVzQQ",
    "track_href": "https://api.spotify.com/v1/tracks/4S8d14HvHb70ImctNgVzQQ",
    "analysis_url": "https://api.spotify.com/v1/audio-analysis/4S8d14HvHb70ImctNgVzQQ",
    "duration_ms": 127947,
    "time_signature": 4
}

def get_energy(af):
    weights = {
        "danceability": 0.1,
        "energy": 0.7,
        "loudness": 0,
        "mode": 0.2,
        "speechiness": 0,
        "acousticness": 0,
        "instrumentalness": 0,
        "liveness": 0,
        "valence": 0
        # "tempo": 0.1
    }
    sum = 0.0
    for key, value in weights.items():
        sum += value
    if sum != 1.0:
        print("invalid weight values, total must be 1.0")
        sys.exit(1)

    energy = 0.0
    for key, value in weights.items():
        energy += af[key] * value

    print("energy: {}".format(energy))

    return energy


def get_positivity(af):
    weights = {
        "danceability": 0.1,
        "energy": 0,
        "loudness": 0,
        "mode": 0.2,
        "speechiness": 0,
        "acousticness": 0,
        "instrumentalness": 0,
        "liveness": 0,
        "valence": 0.7
        # "tempo": 0.1
    }
    sum = 0.0
    for key, value in weights.items():
        sum += value
    if sum != 1.0:
        print("invalid weight values, total must be 1.0")
        sys.exit(1)

    positivity = 0.0
    for key, value in weights.items():
        positivity += af[key] * value

    print("positivity: {}".format(positivity))

    return positivity

def analyse_mood(af):
    energy = get_energy(af)
    positivity = get_positivity(af)
    return (energy, positivity)

print(analyse_mood(af1))
