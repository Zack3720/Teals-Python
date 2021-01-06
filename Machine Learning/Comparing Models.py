from sklearn import datasets
from Logistic import makeModel

dataset = datasets.load_breast_cancer()

makeModel(dataset['target'],dataset['data'])