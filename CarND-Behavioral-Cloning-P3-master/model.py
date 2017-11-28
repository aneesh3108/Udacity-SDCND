#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 12:31:39 2017

@author: aneesh
"""

from keras.layers import Dense, Flatten, Lambda, Activation, MaxPooling2D, Dropout
from keras.layers.convolutional import Conv2D
from keras.models import Sequential
from keras.optimizers import Adam
import json
import inits

Epochs = 8
LR = 1e-4
batch_size = 100
activation = 'elu' # optional replacement: ReLU
 
# loads data       
imgs_path, angles = inits.load_data() 

# balances and clean data for angles to have equal distribution
imgs_path, angles = inits.balance_data(imgs_path, angles, show = False)

#%% Nvidia Model with a slight adjustments to tackle overfitting : Dropout
model = Sequential()

model.add(Lambda(lambda x: x / 127.5 - 1.0, input_shape=(66, 200, 3)))

# starts with five convolutional and maxpooling layers
model.add(Conv2D(24, (5, 5), strides = (2, 2), padding='same'))
model.add(Activation(activation))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))
model.add(Dropout(0.5))

model.add(Conv2D(36, (5, 5), strides = (2, 2), padding='same'))
model.add(Activation(activation))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))
model.add(Dropout(0.5))

model.add(Conv2D(48, (5, 5), strides = (2, 2), padding='same'))
model.add(Activation(activation))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))
model.add(Dropout(0.5))

model.add(Conv2D(64, (3, 3), strides = (1, 1), padding='same'))
model.add(Activation(activation))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))
model.add(Dropout(0.5))

model.add(Conv2D(64, (3, 3), strides = (1, 1), padding='same'))
model.add(Activation(activation))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(1, 1)))
model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(1164))
model.add(Activation(activation))

model.add(Dense(100))
model.add(Activation(activation))

model.add(Dense(50))
model.add(Activation(activation))

model.add(Dense(10))
model.add(Activation(activation))

model.add(Dense(1))

#model.summary()
train_gen = inits.gen_data(imgs_path, angles, batch_size = batch_size)
#
model.compile(optimizer=Adam(LR), loss="mse")
#
history = model.fit_generator(train_gen, steps_per_epoch = round(len(imgs_path)/batch_size), epochs = Epochs, verbose = 1)

#%% Saving the Model
json_string = model.to_json()
with open('model.json', 'w') as outfile:
    json.dump(json_string, outfile)

model.save_weights('model.h5')
#
