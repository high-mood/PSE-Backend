import csv
import sys
from numpy import dot

# These values are associated with the moods used in the research we got our 
# data from. The mapping translates these moods to a 2D-plain of excitement and
# happiness.
energyvector = [9, 3, -7, -2, -8, 9, 6, 7, -7]
happyvector = [8, 5, 5, 5, 1, 2, 9, -4, -8]

with open('./../machinelearning/moods_' + sys.argv[1] + '.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',') 
    outputdata = []
    
    # These values will later be used to rescale the data to rescale the data 
    # to a -9.0-9.0 x -9.0-9.0 square.
    energy_min = energy_max = happiness_min = happiness_max = 0.0
    
    for row in csv_reader:
        # Convert all values to floats.
        for i in range(len(row)):
            row[i] = float(row[i])
        # Dot product to compute the excitement and happiness values.
        new_row = [row[0], dot(row[1:], energyvector), dot(row[1:], happyvector)]
        outputdata.append(new_row)

        energy_min = min(energy_min, new_row[1])
        energy_max = max(energy_max, new_row[1])
        happiness_min = min(happiness_min, new_row[2])
        happiness_max = max(happiness_max, new_row[2])
    
    # Compute values to rescale.
    energy_mean = (energy_max + energy_min) / 2.0
    happiness_mean = (happiness_max + happiness_min) / 2.0
    energy_factor = 9.0 / (energy_max - energy_mean)
    happiness_factor = 9.0 / (happiness_max - happiness_mean)

    # Apply rescale.
    for i in range(len(outputdata)):
        outputdata[i][1] = energy_factor * (outputdata[i][1] - energy_mean)
        outputdata[i][2] = happiness_factor * (outputdata[i][2] - happiness_mean)

with open('./../machinelearning/moods_' + sys.argv[1] + '_translated.csv', "w") as out:
    output = csv.writer(out)
    output.writerows(outputdata)
    
