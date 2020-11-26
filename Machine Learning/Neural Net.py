from sklearn import datasets
import numpy as np
import math
import os

clear = lambda: os.system('cls')
dataset = datasets.load_boston()

targets = dataset['target']
data = dataset['data']
bias = np.ones([len(data),1])
data = np.hstack([data,bias])
weights = None


def find_Guess (inputs):
    global weights
    inputs = inputs * weights
    return inputs.sum()

def find_Weights(data,targets):
    weights = (np.linalg.inv(np.transpose(data).dot(data))).dot(np.transpose(data).dot(targets))
    return weights

def main():
    clear()
    global weights
    np. set_printoptions(suppress=True)
    weights = find_Weights(data,targets)
    sum_of_errors = 0
    largest_error = [0,-1]
    smallest_error = [1000,-1]
    for x in range(len(data)):
        guess = find_Guess(data[x])
        error = targets[x] - guess
        if abs(error) > abs(largest_error[0]):
            largest_error = [error,x]
        if abs(error) < abs(smallest_error[0]):
            smallest_error = [error,x]
        sum_of_errors = error**2

    print('Average Error:')
    print(math.sqrt(sum_of_errors/506))
    print('\nSmallest Error and it\'s index')
    print(smallest_error)
    print('\nLargest Error and it\'s index')
    print(largest_error)
    print('\nWeights:')
    print(weights)
    print('The last one is the bias')
    print('\nFeature Names')
    print(dataset['feature_names'])
    


if __name__ == "__main__":
    main()


