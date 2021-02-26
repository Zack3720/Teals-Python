import numpy as np
import math

def find_Guess (inputs,weights):
    return np.dot(inputs,weights)

def find_Weights(inputs,targets):
    weights = (np.linalg.inv(np.transpose(inputs).dot(inputs))).dot(np.transpose(inputs).dot(targets))
    return weights

def makeModelLinear (targets,inputs):
    inputs = np.hstack([inputs,np.ones([len(inputs),1])])
    weights = find_Weights(inputs,targets)
    errorList = []

    for x in range(len(inputs)):
        guess = find_Guess(inputs[x],weights)
        errorList.append(targets[x] - guess)
    
    return weights
        
    

    #sum_of_errors = 0
    #largest_error = [0,-1]
    #smallest_error = [1000,-1]
    #for x in range(len(inputs)):
    #    guess = find_Guess(inputs[x],weights)
    #    error = targets[x] - guess
    #    if abs(error) > abs(largest_error[0]):
    #        largest_error = [error,x]
    #    if abs(error) < abs(smallest_error[0]):
    #        smallest_error = [error,x]
    #    sum_of_errors += error**2
    #
    #print('Average Error:')
    #print(math.sqrt(sum_of_errors/len(inputs)))
    #print('\nSmallest Error and it\'s index')
    #print(smallest_error)
    #print('\nLargest Error and it\'s index')
    #print(largest_error)
    #print('\nWeights:')
    #print(weights)
    #print('The last one is the bias')
    #print('\nFeature Names')
    #print(inputsset['feature_names'])
    

