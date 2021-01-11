from sklearn import datasets
from Logistic import makeModelLogistic
from Linear import makeModelLinear
import os

clear = lambda: os.system('cls')
clear()

dataset = datasets.load_breast_cancer()

makeModelLogistic(dataset['target'],dataset['data'])