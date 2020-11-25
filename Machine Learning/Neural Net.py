from sklearn import datasets
import numpy as np

data = datasets.load_boston()

target_outputs = data['target']
target_inputs = data['data']
weights = np.ones([1,13])


def find_Guesses (inputs):
    global weights
    bias = np.ones(len(inputs),1)
    inputs = inputs * weights
    inputs = np.hstack(inputs,bias)
    return inputs



