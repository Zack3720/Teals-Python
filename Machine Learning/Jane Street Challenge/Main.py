
# Regression Example With Boston Dataset: Baseline
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
import numpy as np
# load dataset
dataframe = read_csv("Machine Learning\\Jane Street Challenge\\test_set.csv")
dataset = dataframe.to_numpy()
dataset = np.nan_to_num(dataset)
# split into input (X) and output (Y) variables
X = dataset[:,7:]
Y = dataset[:,2:7]
if np.max(Y) > abs(np.min(Y)):
	Y = Y/np.max(Y)
else:
	Y= Y/-np.min(Y)

# define base model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(131, input_dim=131, kernel_initializer='normal', activation='relu'))
	model.add(Dense(10, kernel_initializer='normal'))
	# model.add(Dense(10, kernel_initializer='normal'))
	# model.add(Dense(10, kernel_initializer='normal'))
	# model.add(Dense(10, kernel_initializer='normal'))
	# model.add(Dense(10, kernel_initializer='normal'))
	model.add(Dense(5, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model
# evaluate model
estimator = KerasRegressor(build_fn=baseline_model, epochs=100, batch_size=5, verbose=0)
kfold = KFold(n_splits=5)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Baseline: %.2f (%.2f) MSE" % (results.mean(), results.std()))


# estimator.fit(X,Y)
# Y_predicted = estimator.predict(X)
# acc = np.sign(Y) * np.sign(Y_predicted)
# print( np.sum(acc[acc>0])/np.size(acc))