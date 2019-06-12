import csv
import sys
from numpy import dot

moodmap = [(9,8),(3,5),(-7,5),(-2,5),(-8,1),(9,2),(6,9),(7,-4),(-7,-8)]
energyvector = [9, 3, -7, -2, -8, 9, 6, 7, -7]
happyvector = [8, 5, 5, 5, 1, 2, 9, -4, -8]
with open('./../machinelearning/moods_' + sys.argv[1] + '.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',') 
    outputdata = []
    
    for row in csv_reader:
        for i in range(len(row)):
            row[i] = float(row[i])
        outputdata.append([row[0], dot(row[1:], energyvector), dot(row[1:], happyvector)])

with open('./../machinelearning/moods_' + sys.argv[1] + '_translated.csv', "w") as out:
    output = csv.writer(out)
    output.writerows(outputdata)
    
