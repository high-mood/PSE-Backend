from sklearn.ensemble import GradientBoostingClassifier as GBC
from joblib import load
import numpy as np

''' Mood classification for server, requires the .joblib files imported hereunder.'''

# Load trained models from joblib files
E_est = load('Trained-Energy.joblib')
H_est = load('Trained-Happiness.joblib')

# List of track features.
features = ["mode", "time_signature", "acousticness",
        "danceability", "energy", "instrumentalness", "liveness", "loudness",
        "speechiness", "valence", "tempo"]

def analyseMood(songs):
    input = []
    songtitles = []
    output = []

    for song in songs:
        # Make list of titles.
        songtitles.append(song['songid'])
        # Make list matrix of inpudat data for algorithm.
        inputdata = []
        for feature in features:
            inputdata.append(song[feature])
        input.append(inputdata)

    EnergyPredictions = E_est.predict(input)
    HappinessPredictions = H_est.predict(input)

    # Fill output list with dicts of song id's, energy an happiness values.
    for i in range(len(songtitles)):
        outputdata = {}
        outputdata['songid'] = songtitles[i]
        outputdata['energy'] = EnergyPredictions[i]
        outputdata['happiness'] = HappinessPredictions[i]
        output.append(outputdata)

    return output
        
