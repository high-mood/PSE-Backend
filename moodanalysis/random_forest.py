from sklearn.ensemble import RandomForestClassifier
import numpy as np
import csv
import sys

# Ratio of train / test items from dataset
TRAIN_RATIO = 0.6

'''
Reads data from csv file and returns array of arrays containing that data
'''
def read_data():
    train_set = []
    test_set = []
    with open('./machinelearning/rf_data_20.csv') as csv_file:
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


def random_forest(train_set, test_set):
    clf = RandomForestClassifier(n_jobs=2, n_estimators=10)
    clf.fit([row[1:14] for row in train_set], [row[14] for row in train_set])

    result = clf.predict([row[1:14] for row in test_set])
    succes = 0
    failure = 0
    
    for item in zip(result, [row[14] for row in test_set]):
        if(item[0] == item[1]):
            succes += 1
        else:
            failure += 1
            print("difference is " + str(int(item[1]) - int(item[0])))


    print("succes: " + str(succes))
    print("failure: " + str(failure))


if __name__ == "__main__":
    # input is the ratio.
    if(len(sys.argv) > 1):
        TRAIN_RATIO = float(sys.argv[1])

    # Set static seed and create test and train data
    np.random.seed(0)
    train_set, test_set = read_data()

    random_forest(train_set, test_set)
