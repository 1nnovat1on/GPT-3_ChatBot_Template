import numpy as np

import tensorflow as tf

from keras.models import Sequential

from keras.layers import Dense, Activation

model = Sequential()

model.add(Dense(32, input_dim=784))

model.add(Activation('relu'))

model.add(Dense(10))

model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',

optimizer='sgd',

metrics=['accuracy'])

model.fit(x_train, y_train,

batch_size=128,

nb_epoch=20,

verbose=1,

validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)