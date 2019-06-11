import numpy as np
from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.metrics import r2_score

data = np.array(np.loadtxt(open("PSE-Backend/moodanalysis/machinelearning/parsed_data.csv", "rb"), delimiter=",", skiprows=1))
    
#Prepare training- and test-data    
energy = data[:-20,1]
happiness = data[:-20,2]
traindata = data[:-20, 5:]
testdata = data[-20:, 5:]
testE = data[-20:,1]
testH = data[-20:,2]

print(traindata)
print(energy)
E_est = GBC(n_estimators=11, max_depth=3)
E_est.fit(traindata, energy)
H_est = GBC(n_estimators=11, max_depth=3)
H_est.fit(traindata, happiness)

E_pred = E_est.predict(testdata)
H_pred = H_est.predict(testdata)

for i in range(20):
    # print('Actual Energy: ')
    # print(testE[i])
    # print('Estimated value: ')
    # print(E_pred[i])
    # print('\n')
    print('Actual Happiness: ')
    print(testH[i])
    print('Estimated value: ')
    print(H_pred[i])
    print('\n')
