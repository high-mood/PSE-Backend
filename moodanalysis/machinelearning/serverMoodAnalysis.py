from sklearn.ensemble import GradientBoostingClassifier as GBC
from joblib import load
import numpy as np

E_est = load('Trained-Energy.joblib')
H_est = load('Trained-Happiness.joblib')
features = ["mode", "time_signature", "acousticness",
        "danceability", "energy", "instrumentalness", "liveness", "loudness",
        "speechiness", "valence", "tempo"]

test = [{'songid':'7lR743VxfubUw5m9dpnR9x',
         'artistsids':'6liAMWkVf5LH7YR9yfFy1Y',
         'duration_ms':237973,
         'key':11,
         'mode':1,
         'time_signature':4,
         'acousticness':0.0686,
         'danceability':0.581,
         'energy':0.444,
         'instrumentalness':5.35e-06,
         'liveness':0.0738,
         'loudness':-6.038,
         'speechiness':0.0286,
         'valence':0.233,
         'tempo':78.024,
         'genres':'art pop,electronic,laboratorio,trip hop'}]

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
    for i in range(len(songtitles)):
        outputdata = {}
        outputdata['songid'] = songtitles[i]
        outputdata['energy'] = EnergyPredictions[i]
        outputdata['happiness'] = HappinessPredictions[i]
        output.append(outputdata)
    return output
        
