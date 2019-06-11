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

        # Skip headers.
        next(rows_iter)

        for rows in rows_iter:
            if(np.random.uniform(0, 1) <= TRAIN_RATIO):
                train_set.append(rows)
            else:
                test_set.append(rows)
        
    return train_set,test_set


def somehypenameboi(train_set, test_set):
    clf = RandomForestClassifier(n_jobs=2, random_state=0)
    clf.fit([row[1:14] for row in train_set], [row[14] for row in train_set])

    result = clf.predict([row[1:14] for row in test_set])
    
    for item in zip(result, [row[14] for row in train_set]):
        print( "found: " + str(item[0]) + " correct is: " + str(item[1]))



if __name__ == "__main__":
    # Set static seed and create test and train data
    np.random.seed(0)
    train_set, test_set = read_data()

    somehypenameboi(train_set, test_set)