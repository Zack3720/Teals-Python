from sklearn import datasets
import numpy as np
import math
import os


def makeModelLogistic (targets,inputs):
    data = None
    data = np.hstack([inputs,np.ones([len(inputs),1])])
    weights = np.zeros([len(data[0])])
    errorList = []
    previous_error_average = None
    previous_error_min = None

    while True:
        weights = train_Weights(data,targets,weights,1e-7)
        errorList.append(find_Error(make_Prediction(data,weights),targets))
        if len(errorList) >= 1000:
            current_error_average = np.mean(errorList)
            current_error_min = np.amin(errorList)
            if type(previous_error_average) == type(None):
                previous_error_average = current_error_average
                previous_error_min = current_error_min
            elif (previous_error_average < current_error_average) and (previous_error_min < current_error_min):
                print (errorList[len(errorList)-1])
                print(previous_error_min)
                return previous_error_min
            else:
                previous_error_average = current_error_average
                previous_error_min = current_error_min
            errorList = []
            
            

    return weights

def make_Prediction (inputs,weights):
    results = inputs @ weights
    return np.reciprocal(1 + np.exp(-results))


def train_Weights (inputs,targets,weights,step):
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
