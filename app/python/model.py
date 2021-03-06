# -*- coding: utf-8 -*-

import numpy as np

import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import batch_normalization

def createModel(nbClasses,imageSize):
	print("[+] Creating model...")
	convnet = input_data(shape=[None, imageSize, imageSize, 1], name='input')

	#Add loss function dependent on class sizes 

	convnet = conv_2d(convnet, 64, 2, activation='elu', weights_init="Xavier", name='conv1')
	#convet = batch_normalization(convnet, trainable=True)#, restore=True)
	convnet = max_pool_2d(convnet, 2)
	
	convnet = conv_2d(convnet, 128, 2, activation='elu', weights_init="Xavier", name='conv2')
	#convet = batch_normalization(convnet, trainable=True)#, restore=True)
	convnet = max_pool_2d(convnet, 2)

	convnet = conv_2d(convnet, 256, 2, activation='elu', weights_init="Xavier", name='conv3')
	#convet = batch_normalization(convnet, trainable=True)#, restore=True)
	convnet = max_pool_2d(convnet, 2)

	convnet = conv_2d(convnet, 512, 2, activation='elu', weights_init="Xavier", name='conv4')
	#convet = batch_normalization(convnet, trainable=True)
	convnet = max_pool_2d(convnet, 2)

	convnet = fully_connected(convnet, 1024, activation='elu')
	convnet = dropout(convnet, 0.5)
	
	convnet = fully_connected(convnet, nbClasses, activation='softmax')
	convnet = regression(convnet, optimizer='adam', loss='categorical_crossentropy')

	model = tflearn.DNN(convnet)
	print("    Model created! ✅")
	return model
