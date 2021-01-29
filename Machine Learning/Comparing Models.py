from sklearn import datasets
from Logistic import makeModelLogistic
from Logistic import make_Prediction
from Linear import makeModelLinear
from Linear import find_Guess
import numpy as np
import os

clear = lambda: os.system('cls')
clear()

dataset = datasets.load_breast_cancer()

data = dataset['data']
targets = dataset['target']

logisticWeights = makeModelLogistic(targets,data)
linearWeights = makeModelLinear(targets,data)

data = np.hstack([data,np.ones([len(data),1])])

logisticErrorList = abs(make_Prediction(data,logisticWeights) - targets)
linearErrorList = abs(targets - find_Guess(data,linearWeights))**2

print('Average Logistic Error: ' + str(logisticErrorList.mean()))
print('Average Linear Error: ' + str(linearErrorList.mean()))