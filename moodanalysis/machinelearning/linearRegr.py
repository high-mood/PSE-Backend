import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

data = np.array(np.loadtxt(open("PSE-Backend/moodanalysis/machinelearning/parsed_data.csv", "rb"), delimiter=",", skiprows=1))
    
# Prepare training- and test-data    
energy = data[:-20,1]
happiness = data[:-20,2]
traindata = data[:-20, 5:]
testdata = data[-20:, 5:]
testE = data[-20:,1]
testH = data[-20:,2]

# Fit training-data
regE = LinearRegression()
regE.fit(traindata, energy)
regH = LinearRegression()
regH.fit(traindata, happiness)

# Make predictions
E_pred = regE.predict(testdata)
H_pred = regH.predict(testdata)

# Assign scores
E_score = r2_score(testE, E_pred)
H_score = r2_score(testH, H_pred)

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
