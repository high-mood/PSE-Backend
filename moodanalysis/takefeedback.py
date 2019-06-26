def write_feedback(userfeedback):
    '''No longer used --- Writes userfeedback to a csv file which can be used to retrain
    the ML-model
    :param userfeedback: [id, energy, happiness, durations_ms, key, mode, time_signature,
    acoustiness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo]'''
    import csv
    if (len(userfeedback) != 16 or type(userfeedback) != list):
        # May need different error handling on server
        raise ValueError
    with open('userfeedback.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(userfeedback)
