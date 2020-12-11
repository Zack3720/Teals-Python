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
    results = inputs * weights
    return (1/1 + math.e**(-results.sum(1)))

def train_Weights(inputs,targets,weights,step):
    # wt+1 = wt - a(XT(y’ - y))
    results = make_Prediction(inputs,weights)
    results = results - targets
    results = data.transpose() @ results
    results = step * results
    results = weights - results
    print(results.shape)
    return results
    #return weights - step @ (data.transpose() @ (make_Prediction(data,weights)-targets))

def find_Error(predicted,targets):
    #  ( y * ln(y’) + (1 - y) * ln(1 - y’) )
    predicted += 10**-15
    return (targets * np.log(predicted) + (1-targets) * np.log(1-predicted)).sum()

weights = np.ones([len(data[0])])
previousError = 1000
Error = 0
print(data.shape)
print(weights.shape)

while previousError - Error > 0.1:
    previousError = Error
    weights = train_Weights(data,targets,weights,0.1)
    Error = find_Error(make_Prediction(data,weights),targets)
    print(str(Error))