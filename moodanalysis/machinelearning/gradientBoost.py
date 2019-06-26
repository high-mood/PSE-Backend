import numpy as np
from sklearn.ensemble import GradientBoostingRegressor as GBR
import csv
from joblib import dump, load


def main(TRAIN_RATIO):
    ''' This script is used to train the Gradient Boosting Regressor. 
    The .joblib files (trained data) are used on the server for
    mood analysis. This file is only used offline.
    :param TRAIN_RATIO: Ratio used to train/test the data'''

    data = np.array(np.loadtxt(open("analyzed_tracks_1.csv", "rb"),
                               delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5, 6, 7, 8, 9,
                                                                   10, 11, 12, 13, 14, 15)))

    trainset = []
    testset = []

    for item in data:
        if(np.random.uniform(0, 1) <= TRAIN_RATIO):
            trainset.append(item)
        else:
            testset.append(item)

    energy = [elem[0] for elem in trainset]
    happiness = [elem[1] for elem in trainset]
    traindata = [elem[4:] for elem in trainset]
    testdata = [elem[4:] for elem in testset]
    testE = [elem[0] for elem in testset]
    testH = [elem[1] for elem in testset]

    E_est = GBR(n_estimators=50, max_depth=3)
    E_est.fit(traindata, energy)
    H_est = GBR(n_estimators=50, max_depth=3)
    H_est.fit(traindata, happiness)

    # Create .joblib files to reuse the trained algorith later.
    dump(E_est, 'Trained-Energy.joblib')
    dump(H_est, 'Trained-Happiness.joblib')

    E_pred = E_est.predict(testdata)
    H_pred = H_est.predict(testdata)

    # Determine absolute difference betweeen predictions and actual values.
    E_sum = 0
    H_sum = 0

    for i in range(len(testE)):
        difE = abs(testE[i]-E_pred[i])
        difH = abs(testH[i]-H_pred[i])
        E_sum += difE
        H_sum += difH
    print(E_sum, H_sum)


if __name__ == "__main__":
    main(0.75)
