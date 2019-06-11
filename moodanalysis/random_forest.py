from sklearn.ensemble import RandomForestClassifier
import numpy as np
import csv

# Ratio of train / test items from dataset
TRAIN_RATIO = 0.75

'''
Reads data from csv file and returns array of arrays containing that data
'''
def read_data():
    train_set = []
    test_set = []
    with open('./machinelearning/rf_data.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rows_iter = iter(csv_reader)

        # Add headers to both datasets.
        headeres = next(rows_iter)
        train_set.append(headeres)
        test_set.append(headeres)

        for rows in rows_iter:
            if(np.random.uniform(0, 1) <= TRAIN_RATIO):
                train_set.append(rows)
            else:
                test_set.append(rows)
        
    return train_set,test_set


if __name__ == "__main__":
    # Set static seed and create test and train data
    np.random.seed(0)
    train_set, test_set = read_data()