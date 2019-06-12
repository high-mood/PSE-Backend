""" This python file reads the data.csv from http://www2.projects.science.uu.nl/memotion/emotifydata/
The data is added and put into a list of lists (data) which we can use for training our Machine Learning
algorithm for mood analysis. Another Python file supplied by Barry scrapes the spotify API for audio-features
related to these tracks. In this way we can compare interviewees opinions to spotify's supplied parameters."""
import csv

with open('./../machinelearning/data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    iterrows = iter(csv_reader)
    next(iterrows)
    numericdata = []
    for row in csv_reader:
        del row[1]
        del row[15]
        for i in range(15):
            row[i] = int(row[i])
        numericdata.append(row)
    data = []
    list_count = 0
    new_data = [0 for i in range(13)]
    numberofresponses = [0 for i in range(401)]
    for row in numericdata:
        if row[0] > list_count:
            if(numberofresponses[list_count - 1] >= 20):
                data.append(new_data)
                new_data = [0 for i in range(13)]
            list_count += 1
            numberofresponses[list_count] += 1
        else:
            numberofresponses[list_count-1] += 1
            for i in range(13):
                new_data[i] += row[i+1]
    for i in range(len(data)):
        print("Song: ")
        print(data[i][0])
        print("Data gathered: ")
        print(data[i])
        print("Number of responses: ")
        print(numberofresponses[i])
        print("\n\n")
