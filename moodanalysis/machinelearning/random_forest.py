from sklearn.ensemble import RandomForestRegressor as RFR
import numpy as np
import csv
import sys

# Ratio of train / test items from dataset
TRAIN_RATIO = 0.6

def read_data(bound):
    ''' Read the input data from the analyzed_tracks_'bound'.csv file. Returns a train
    and test set based on the data in this file.

    params:
    bound: lower bound on song reviews.

    returns:
    train_set: Data to train algorithm.
    test_set: Data to test algorithm.
    '''
    train_set = []
    test_set = []

    with open('./machinelearning/analyzed_tracks_' + str(bound) +'.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rows_iter = iter(csv_reader)

        # Skip headers.
        next(rows_iter)

        # Randomly create test and train sets.
        for rows in rows_iter:
            if(np.random.uniform(0, 1) <= TRAIN_RATIO):
                train_set.append(rows)
            else:
                test_set.append(rows)

    return train_set,test_set


def random_forest(train_set, test_set):
    ''' Creates, trains and tests a random forest regressor, then writes results
    to terminal.

    Params:
    train_set: A list with training data.
    test_set: A list with test data.
    '''
    clf_energy = RFR(n_jobs=2, n_estimators=10)
    clf_happiness = RFR(n_jobs=2, n_estimators=10)

    # Fit the regressor models on the spotify statistics, fit them on the
    # mood stats determined by another research project.
    clf_energy.fit([row[3:16] for row in train_set], [row[1] for row in train_set])
    clf_happiness.fit([row[3:16] for row in train_set], [row[2] for row in train_set])

    result_energy = clf_energy.predict([row[3:16] for row in test_set])
    result_happiness = clf_happiness.predict([row[3:16] for row in test_set])

    # Compute the total absolute difference between the predicted and actual
    # moods.
    energy_mean = 0.0
    happiness_mean = 0.0
    for i in range(len(test_set)):
        energy_mean += abs(float(result_energy[i]) - float(test_set[i][1]))
        happiness_mean += abs(float(result_happiness[i]) - float(test_set[i][2]))

    energy_mean /= len(test_set)
    happiness_mean /= len(test_set)

    print("Avg discrepancy - Energy: " + str(energy_mean))
    print("Avg discrepancy - Happiness: " + str(happiness_mean))

if __name__ == "__main__":
    # First input is the lower bound on votes per song.
    if(len(sys.argv) <2):
        print('please give the vote lower bound')
        exit()

    # Second input is the train/test ratio (optional).
    if(len(sys.argv) > 2):
        TRAIN_RATIO = float(sys.argv[2])

    # Set static seed and create test and train data
    # np.random.seed(0)
    bound = int(sys.argv[1])

    train_set, test_set = read_data(bound)
    random_forest(train_set, test_set)
