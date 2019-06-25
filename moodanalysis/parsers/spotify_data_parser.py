""" This python file reads moods.csv and the songs folder. Then it attempts to
find the song on spotify, get its metrics and stores thse values in a csv called
test_data.csv. On error the song is skipped."""

from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from time import sleep
from datetime import datetime
import requests
import sys

def add_audio_features(id, token, endpoint="https://api.spotify.com/v1/audio-features/"):
    '''
    Find song features for given song.

    Params:
    id:         identifier of song
    token:      oath token for spotify
    endpoint:   spotify api adress, default is the audio-features api

    Return:
    Dict of dicts that hold song features.
    '''
    # Get data from spotify.
    r = requests.get(endpoint + id, headers={"Authorization": f"Bearer {token}"})
    audio_features = r.json()
    
    if(r.status_code != 200):
        return None

    # Return key features.
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
                    "tempo": audio_features["tempo"],
                    "id": audio_features["id"]}

    return feature_set

def get_track_id(song_name, song_artist, token, endpoint="https://api.spotify.com/v1/search"):
    '''
    Finds spotify song id for given song, returns None if data could not be found.

    Params:
    song_name:    name of song
    song_artist:  main artist of song
    token:        oath token of spotify
    endpoint:     spotify api adress, default is the search api

    Returns:
    Track identifier for spotify, song name
    '''
    # Attempt to get track id by trying the first track in combination with 
    # the artist.
    r = requests.get(endpoint + "?query=" + song_name.strip().replace(" ", "+") + "&type=track", headers={"Authorization": f"Bearer {token}"})
    track = r.json()
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        quit()

    if len(track["tracks"]["items"]) > 0 and len(track["tracks"]) > 0:
         return track["tracks"]["items"][0]["id"], song_name.replace(",", "")
    return None, None



def get_track_features(token):
    '''
    Function that retrieves track features for songs in database.

    Params:
    token: oath token of spotify

    Return:
    Dict of dicts that contains the features for all songs.
    '''

    # Hardcoded names of directories that contain the songs.
    folders = ["classical", "rock", "pop", "electronic"]
    song_info = {folder: {} for folder in folders}

    # Retrieve song and artist from mp3 file. Loop over all 100 songs per dir.
    for folder in folders:
        for index in range(1,101):
            mp3 = MP3File("./../../../songs/" + folder + "/" + str(index) + ".mp3")
            mp3.set_version(VERSION_2)

            # Retrieve song information from spotify
            id, song_name = get_track_id(mp3.song, mp3.artist, token)
            if(id != None):
                # put audio features in dict.
                audio_features = add_audio_features(id, token)
                audio_features["name"] = song_name
                song_info[folder][str(index)] = audio_features
            # this sleep prevents the api from being queried too often.
            sleep(0.10)

    return song_info

def match_moods_features(track_feature_dict):
    '''
    Match moods from previous analysises with spotifies metrics. Writes everything
    to a csv.

    Params:
    track_feature_dict: Dict that matches track id + genre to spotify metrics.
    '''

    # CSV with moods.
    moods_csv = open("./../machinelearning/moods_" + sys.argv[2] +"_translated.csv", "r")
    # CSV to store results.
    analyzed_tracks_csv = open("./../machinelearning/analyzed_tracks_" + sys.argv[2] +".csv", "w+")

    # translation table for indexes.
    trans_table = ["classical", "rock", "electronic", "pop"]
    # List of features in json object.
    feature_set = ["duration_ms", "key", "mode", "time_signature", "acousticness",
        "danceability", "energy", "instrumentalness", "liveness", "loudness",
        "speechiness", "valence", "tempo", "name"]
    
    analyzed_tracks_csv.write("songid,excitedness,happiness")
    for item in feature_set:
        analyzed_tracks_csv.write("," + item)
    analyzed_tracks_csv.write(",response_count,response_excitedness,response_happiness")    
    analyzed_tracks_csv.write("\n")

    for line in moods_csv:
        # First item is number, second energy and finally happiness.
        parts = line.split(",")

        # Data in csv is formatted wrong.
        if (len(parts) != 3):
            print("Number of items in line is not 3?")
            continue

        # Match track id in csv with track in folder.
        index = int(float(parts[0]))
        features = track_feature_dict[trans_table[(int((index-1)/100 - 1))]].get(str(int(((index-1) % 100) + 1)), None)

        if(not features is None):
            # Write data to csv file.
            analyzed_tracks_csv.write(features["id"] + "," + parts[1] + "," + parts[2].strip())
            for feature in feature_set:
                analyzed_tracks_csv.write("," + str(features[feature]))

            analyzed_tracks_csv.write(f",20,{parts[1]},{parts[2].strip()}")
            analyzed_tracks_csv.write("\n")


if __name__ == "__main__":
    # Check input arguments, first should be token for spotify API.
    if(len(sys.argv) < 2):
        print("No token and lower bound for vote count given")
        exit()

    # Check input arguments, second should be vote bound.
    if(len(sys.argv) < 3):
        print("No lower bound vote bount given")
        exit()
    
    token = sys.argv[1]

    r = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {token}"})
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        quit()

    track_feature_dict = get_track_features(token)
    match_moods_features(track_feature_dict)
    