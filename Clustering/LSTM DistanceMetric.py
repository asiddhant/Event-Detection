import numpy
import re
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,LSTM
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


## Reading the Vector File
# The file must be in current directory
file = pd.read_csv("newsVectors.csv")
I = numpy.array(file.ix[:file.shape[1]-1])
MD = I[:,:I.shape[1]/2]-I[:,I.shape[1]/2+1:]
DP = I[:,:I.shape[1]/2]*I[:,I.shape[1]/2+1:]
X = numpy.concatenate([MD,DP],1)
Y = numpy.array(file.ix[])


## Defining the LSTM Model
# We have used Dropout for Regularization
model = Sequential()
model.add(LSTM(512, input_shape=(X.shape[0], X.shape[1])))
model.add(Dropout(0.5))
model.add(LSTM(256, input_shape=(X.shape[0], X.shape[1])))
model.add(Dropout(0.5))
model.add(LSTM(128, input_shape=(X.shape[0], X.shape[1])))
model.add(Dropout(0.5))
model.add(Dense(Y.shape[1], activation='softmax'))

optimizer = RMSprop(lr=0.02)
model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Checkpoint Definition : Save weights if there is an improvement at iterations
filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

# Number of epochs has been set to 10. Each epoch takes about 10000 seconds
model.fit(X, Y, nb_epoch=20, batch_size=128, callbacks=callbacks_list)


# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
