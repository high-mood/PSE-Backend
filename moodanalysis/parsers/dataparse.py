""" This python file reads the data.csv from http://www2.projects.science.uu.nl/memotion/emotifydata/
The data is added and put into a list of lists (data) which we can use for training our Machine Learning
algorithm for mood analysis. Another Python file supplied by Barry scrapes the spotify API for audio-features
related to these tracks. In this way we can compare interviewees opinions to spotify's supplied parameters."""
import csv

with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    iterrows = iter(csv_reader)
    next(iterrows)
    numericdata = []
    #Iterate over all columns except text and map strings -> int
    for row in csv_reader:
        del row[1]
        for i in range(6):
            del row[10]
        for i in range(10):
            row[i] = int(row[i])
        numericdata.append(row)
    data = []
    list_count = 0
    numberofresponses = [0 for i in range(401)]
    # Add together responses on same song
    for row in numericdata:
        gradesum = sum(row[1:])
        if gradesum == 0:
            gradesum = 1
        n = row[0]
        if row[0] > list_count:
            normrow = [n] + [x/gradesum for x in row[1:]]
            data.append(normrow)
            list_count += 1
            numberofresponses[list_count] += 1
        else:
            numberofresponses[list_count-1] += 1
            for i in range(8):
                data[list_count-1][i+1] += (row[i+1]/gradesum)
    #Normalizing data
    for i in range(len(data)):
        for j in range(8):
            data[i][j+1] = round(data[i][j+1]/numberofresponses[i], 2)

with open('testnorm.csv', "w") as out:
    output = csv.writer(out)
    output.writerows(data)
