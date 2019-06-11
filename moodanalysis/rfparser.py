"""This python file reads the data from test_data.csv and transforms the 
happiness, energy tuple into an integer. The lower left corner is 0, the lower 
right corner is 7, the upper right corner is 63. The grid consists of 2.5 by 2.5 
blocks. This way we can use the data for a random forest algorithm."""

from math import trunc
import csv

data = []

with open("./machinelearning/test_data.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    iterrows = iter(csv_reader)

    titles = next(iterrows)
    del titles[2]
    del titles[1]
    titles.append("location")
    data.append(titles)
    
    for row in csv_reader:
        # Computation to map points in grid.
        x_result = min(int(trunc((float(row[1]) + 10.0) / 2.5)), 7)
        y_result = min(int(trunc((float(row[2]) + 10.0) / 2.5)), 7)
        location = 8 * y_result + x_result

        # Delete redundant rows.
        del row[2]
        del row[1]

        # Add new data.
        row.append(location)
        data.append(row)


with open("./machinelearning/rf_data.csv", 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerows(data)
    

