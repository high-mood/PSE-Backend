from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from time import sleep
from datetime import datetime
import requests
import sys

# Retrieve data from spotify api

'''
Find song features for given song.

Parameters:
id    - identifier of song
token - oath token for spotify

Return
Dict of dicts that hold song features.
'''
def add_audio_features(id, token, endpoint="https://api.spotify.com/v1/audio-features/"):
    r = requests.get(endpoint + id, headers={"Authorization": f"Bearer {token}"})
    audio_features = r.json()

    feature_set = {"duration_ms": audio_features["duration_ms"],
                    "key": audio_features["key"],
                    "mode": audio_features["mode"],
                    "time_signature": audio_features["time_signature"],
                    "acousticness": audio_features["acousticness"],
                    "danceability": audio_features["danceability"],
                    "energy": audio_features["energy"],
                    "instrumentalness": audio_features["instrumentalness"],
                    "liveness": audio_features["liveness"],
                    "loudness": audio_features["loudness"],
                    "speechiness": audio_features["speechiness"],
                    "valence": audio_features["valence"],
                    "tempo": audio_features["tempo"]}

    return feature_set


'''
Finds spotify song id for given song, returns None if data could not be found.

Parameters:
song_name    - name of song
song_artist  - main artist of song
token        - oath token of spotify

Return:
track identifier for spotify
'''
def get_track_id(song_name, song_artist, token, endpoint="https://api.spotify.com/v1/search"):

    r = requests.get(endpoint + "?query=" + song_name.strip().replace(" ", "+") + "&type=track", headers={"Authorization": f"Bearer {token}"})
    track = r.json()
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        quit()

    if len(track["tracks"]["items"]) > 0 and len(track["tracks"]) > 0:
         return track["tracks"]["items"][0]["id"]
    return None


'''
Function that retrieves track features for songs in database.

Parameters:
token - oath token of spotify

Return:
Dict of dicts that contains the features for all songs.
'''
def get_track_features(token):

    # Hardcoded names of directories that containt he songs
    folders = ["classical", "rock", "pop", "electronic"]
    song_info = {folder: {} for folder in folders}

    # Retrieve song and artist from mp3 file. Loop over all 100 songs per dir.
    for folder in folders:
        for index in range(1,101):
            mp3 = MP3File("./../songs/" + folder + "/" + str(index) + ".mp3")
            mp3.set_version(VERSION_2)

            # Retrieve song information from spotify
            id = get_track_id(mp3.song, mp3.artist, token)
            if(id != None):
                # put audio features in dict.
                song_info[folder][str(index)] = add_audio_features(id, token)
            # this sleep prevents the api from being queried too often.
            sleep(0.10)

    return song_info

# Match track features with moods.

'''
Match moods from previous analysises with spotifies metrics. Writes everything
to a csv.

Parameters:
Dict that matches track id + genre to spotify metrics.
'''
def match_moods_features(track_feature_dict):
    # CSV with moods.
    moods_csv = open("moods.csv", "r")
    # CSV to store results in.
    analyzed_tracks_csv = open("analyzed_tracks.csv", "w+")

    # translation table for indexes.
    trans_table = ["classical", "rock", "electronic", "pop"]
    # List of features in json object.
    feature_set = ["duration_ms", "key", "mode", "time_signature", "acousticness",
        "danceability", "energy", "instrumentalness", "liveness", "loudness",
        "speechiness", "valence", "tempo"]

    for line in moods_csv:
        # First item is number, second energy and finally happiness.
        parts = line.split(",")

        if (parts.len != 3):
            # something is wrong with this line
            print("Number of items in line is not 3?")
            continue
        
        index = int(parts[0])        

        features = track_feature_dict[trans_table[(index-1)/100 - 1]][((index-1) % 100) + 1]
        if( features is None):
            continue

        # Write data to csv file.
        analyzed_tracks_csv.write(parts[0] + "," + parts[1] + "," + parts[2])
        for feature in feature_set:
            analyzed_tracks_csv.write("," + features[feature])
        analyzed_tracks_csv.write("\n")


if __name__ == "__main__":
    token = sys.argv[1]

    r = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {token}"})
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        quit()

    user_id = r.json()["id"]

    track_feature_dict = get_track_features(token)
    match_moods_features(track_feature_dict)
    