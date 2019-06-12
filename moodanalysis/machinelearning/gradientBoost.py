import numpy as np
from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.metrics import r2_score
import csv

TRAIN_RATIO = 0.75
data = ((np.array(np.loadtxt(open("parsed_data.csv", "rb"), delimiter=",", skiprows=1)))*100).astype(int)
#Prepare training- and test-data
trainset = []
testset = []

for item in data:
    if(np.random.uniform(0, 1) <= TRAIN_RATIO): 
        trainset.append(item)
    else:
        testset.append(item)

energy = [elem[1] for elem in trainset]
happiness = [elem[2] for elem in trainset]
traindata = [elem[5:] for elem in trainset]
testdata = [elem[5:] for elem in testset]
testE = [elem[1] for elem in testset]
testH = [elem[2] for elem in testset]

E_est = GBC(n_estimators=50, max_depth=3)
E_est.fit(traindata, energy)
H_est = GBC(n_estimators=50, max_depth=3)
H_est.fit(traindata, happiness)

E_pred = E_est.predict(testdata)
H_pred = H_est.predict(testdata)

E_sum = 0
H_sum = 0

for i in range(20):
    E_sum += abs(testE[i]-E_pred[i])
    H_sum += abs(testH[i]-H_pred[i])

    print('Actual Energy: ')
    print(testE[i])
    print('Estimated value: ')
    print(E_pred[i])
    print('\n')
    print('Actual Happiness: ')
    print(testH[i])
    print('Estimated value: ')
    print(H_pred[i])
    print('\n')
print(E_sum, H_sum)
print("Avg discrepancy - Energy:")
print(E_sum/len(testE))
print("Avg discrepancy - Happiness:")
print(H_sum/len(testE))
