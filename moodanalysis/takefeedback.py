'''This file can be used to append user feedback to the training set for the ML algorithm in order to
improve mood-analysis. The function writefeedback should take a list of the following format:
[id, energy, happiness, durations_ms, key, mode, time_signature, acoustiness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo]'''

def writefeedback(userfeedback):
    import csv
    if (len(userfeedback) != 16 or type(userfeedback) != list):
        raise ValueError
    with open('test.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(userfeedback)
