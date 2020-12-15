from sklearn import datasets
import numpy as np
import math
import os

clear = lambda: os.system('cls')
clear()

dataset = datasets.load_breast_cancer()

targets = dataset['target']
data = None
data = np.hstack([dataset['data'],np.ones([len(dataset['data']),1])])


def make_Prediction (inputs,weights):
    results = inputs @ weights
    return np.reciprocal(1 + np.exp(-results))


def train_Weights(inputs,targets,weights,step):
    # wt+1 = wt - a(XT(y’ - y))
    results = make_Prediction(inputs,weights)
    results = results - targets
    results = inputs.transpose() @ results
    results = step * results
    results = weights - results
    return results
    #return weights - step @ (data.transpose() @ (make_Prediction(data,weights)-targets))

def find_Error(predicted,targets):
    #  ( y * ln(y’) + (1 - y) * ln(1 - y’) )
    predicted[predicted < 1e-15] = 1e-15
    predicted[predicted > (1 - 1e-15)] = 1 - 1e-15
    return -(targets * np.log(predicted) + (1-targets) * np.log(1-predicted)).sum()

weights = np.zeros([len(data[0])])
previousError = 0
Error = 0

for x in range(5000):
    previousError = Error
    weights = train_Weights(data,targets,weights,1e-7)
    Error = find_Error(make_Prediction(data,weights),targets)
    print(str(Error))