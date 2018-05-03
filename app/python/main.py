# -*- coding: utf-8 -*-
import random
import string
import os
import sys
import glob
import numpy as np
import tensorflow as tf
from PIL import Image
import os.path

from model import createModel
from datasetTools import getDataset
from config import slicesPath
from config import predictionPath, predictSpect, predSlicePath
from config import batchSize
from config import filesPerGenre
from config import nbEpoch
from config import validationRatio, testRatio
from config import sliceSize
from config import genreList

from songToData import createSlicesFromAudio
from audioFilesTools import isMono
from imageFilesTools import getImageData
from subprocess import Popen, PIPE, STDOUT
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from numpy import array
from library import library
from library import song
from knn import kNNclassify
import hypertools as hyp

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="Trains, tests, predicts the CNN", nargs='+', choices=["train","test","slice", "predict", "classify"])
args = parser.parse_args()

currentPath = os.path.dirname(os.path.realpath(__file__)) 

print("--------------------------")
print("| ** Config ** ")
print("| Validation ratio: {}".format(validationRatio))
print("| Test ratio: {}".format(testRatio))
print("| Slices per genre: {}".format(filesPerGenre))
print("| Slice size: {}".format(sliceSize))
print("--------------------------")

if "slice" in args.mode:
	createSlicesFromAudio()
	sys.exit()

#List genres
genres = os.listdir(slicesPath)
genres = [filename for filename in genres if os.path.isdir(slicesPath+filename)]
nbClasses = len(genres)

#Create model
model = createModel(nbClasses, sliceSize)
#test_X, test_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="test")
#validation_monitor = tf.contrib.learn.monitors.ValidationMonitor(test_X, test_y, every_n_steps=50)
#model2 = createFCModel(nbClasses, sliceSize)

if "train" in args.mode:
	
	#Create or load new dataset
	train_X, train_y, validation_X, validation_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="train")

	#Define run id for graphs
	run_id = "MusicGenres - "+str(batchSize)+" "+''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(8))

	#Train the model
	print("[+] Training the model...")
	model.fit(train_X, train_y, n_epoch=nbEpoch, batch_size=batchSize, shuffle=True, validation_set=(validation_X, validation_y), snapshot_step=100, show_metric=True, run_id=run_id)
	print("    Model trained! ✅")

	#Save trained model
	print("[+] Saving the weights...")
	model.save('musicDNN.tflearn')
	print("[+] Weights saved! ✅💾")

if "test" in args.mode:

	#Create or load new dataset
	test_X, test_y = getDataset(filesPerGenre, genres, sliceSize, validationRatio, testRatio, mode="test")
	
	#Load weights
	print("[+] Loading weights...")
	model.load('musicDNN.tflearn')
	print("    Weights loaded! ✅")

	testAccuracy = model.evaluate(test_X, test_y)[0]
	print("[+] Test accuracy: {}".format(testAccuracy))

if "predict" in args.mode:

	#get name of input file to predict
	userinput = raw_input('Input a file to predict genre: ')
	#userinput = 'Classical_4'
	userinput += '.mp3'
	
	newFilename = 'new_' + userinput
	newFilename = newFilename.replace(".mp3", "")
	if(isMono(userinput)):
		command = "cp '{}' '/tmp/{}.wav'".format(userinput,newFilename)
	else:
		command = "sox '{}' '/tmp/{}.wav' remix 1,2".format(userinput,newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print (errors)

	newSpecPath = 'New_Spectrograms/'
	#Create path if not existing
	if not os.path.exists(os.path.dirname(newSpecPath)):
		try:
			os.makedirs(os.path.dirname(newSpecPath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#create spectrogram from given file
	userinput.replace(".mp3","")
	print ("Creating spectrogram for file {}".format(userinput))
	command = "sox '/tmp/{}.wav' -n spectrogram -Y 200 -X 50 -m -r -o '{}.png'".format(newFilename,newSpecPath+newFilename)
	p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
	output, errors = p.communicate()
	if errors:
		print (errors)

	#Remove tmp mono track
	os.remove("/tmp/{}.wav".format(newFilename))

	desiredSize = 128
	name = "new"
	#slice spectrogram
	for newFilename in os.listdir(newSpecPath):
		if newFilename.endswith(".png"):
			#slice
			img = Image.open(newSpecPath+newFilename)

			width, height = img.size
			nbSamples = int(width/desiredSize)
			width - desiredSize
			#Create path if not existing
			slicePath = "newSlicePath/"
			if not os.path.exists(os.path.dirname(slicePath)):
				try:
					os.makedirs(os.path.dirname(slicePath))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise
			
			#For each sample
			for i in range(nbSamples):
				print ("Creating slice: ", (i+1), "/", nbSamples, "for", newFilename)
				#Extract and save 128x128 sample
				startPixel = i*desiredSize
				imgTmp = img.crop((startPixel, 1, startPixel + desiredSize, desiredSize + 1))
				imgTmp.save(slicePath+"new/{}_{}.png".format(newFilename[:-4],i))


	#load each image slice with given prefix with getImageData method
	data = []
	spect_files = glob.glob('newSlicePath/new/*.png')
	#append each loaded image slice to a data-array

	for file in spect_files:
		img_array = getImageData(file, sliceSize)
		print (file)
		data.append(img_array)
		os.remove(file) #remove slices

	os.remove(newSpecPath + newFilename) #remove spectrogram
	print('Analyzing file...')

	#load model and get predictions
	model.load('musicDNN.tflearn')
	predictionSoftmax = model.predict(data)[0]
	predictedIndex = max(enumerate(predictionSoftmax), key=lambda x:x[1])[0]
	print (predictionSoftmax,'\n')
	
	print ("Prediction:", ["{0:.2f}".format(x) for x in predictionSoftmax], "->", predictedIndex)
	pGenre = genres[predictedIndex]
	print("The genre is: %s" % pGenre)
	

if "classify" in args.mode:

	#create spectrogram path if it doesn't exist
	if not os.path.exists(os.path.dirname(predictSpect)):
		try:
			os.makedirs(os.path.dirname(predictSpect))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	#create slice path if it doesn't exist
	if not os.path.exists(os.path.dirname(predSlicePath)):
		try:
			os.makedirs(os.path.dirname(predSlicePath))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	counter = 0

	print ("Creating Spectrogams")
	#parse through all files in library and create spectrograms
	for filename in os.listdir(predictionPath):
		if filename.endswith(".mp3"):
			newFilename = 'new_' + filename
			newFilename = newFilename.replace(".mp3", "")
			
			if(isMono(predictionPath+filename)):
				command = "cp '{}' '/tmp/{}.wav' remix 1,2".format(predictionPath+filename, newFilename)
			else:
				command = "sox '{}' '/tmp/{}.wav' remix 1,2".format(predictionPath+filename,newFilename)
			p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
			output, errors = p.communicate()
			if errors:
				print (errors)

			#create spectrogram from given file
			filename.replace(".mp3","")
			#print "Creating spectrogram for file {}".format(filename)
			command = "sox '/tmp/{}.wav' -n spectrogram -Y 200 -X 50 -m -r -o '{}.png'".format(newFilename,predictSpect+newFilename)
			p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
			output, errors = p.communicate()
			if errors:
				print (errors)

			#Remove tmp mono track
			os.remove("/tmp/{}.wav".format(newFilename))
			counter += 1

	subdata = []
	data = []

	print ("Spectrogams Created! ✅")
	#slice spectrograms
	
	print ("Slicing Spectrogams")
	for newFilename in os.listdir(predictSpect):
		if newFilename.endswith(".png"):
			#slice
			img = Image.open(predictSpect+newFilename)

			width, height = img.size
			nbSamples = int(width/sliceSize)
			width - sliceSize

			#For each sample
			for i in range(nbSamples):
				#print "Creating slice: ", (i+1), "/", nbSamples, "for", newFilename
				#Extract and save 128x128 sample
				startPixel = i*sliceSize
				imgTmp = img.crop((startPixel, 1, startPixel + sliceSize, sliceSize + 1))
				imgTmp.save(predSlicePath+"{}_{}.png".format(newFilename[:-4],i))

				img_array = getImageData(predSlicePath+newFilename[:-4]+"_"+str(i)+".png", sliceSize)
				
				#append each loaded image to a sub-data array, and break to new subdata element when name changes
				subdata.append(img_array)
				#os.remove()
			
			#append sub-data array to super array
			data.append(subdata)
			subdata = []


	print ("Slices Created! ✅")

	model.load('musicDNN.tflearn')
	print ("Model loaded! ✅")
	s = song()
	lib = library()

	#print data

	#parse through super array predicting each one 
	#and assign name to song object then append song object to songList in library
	print ("Predicting")
	for vec in data:
		predictionSoftmax = model.predict(vec)[0]
		predictedIndex = max(enumerate(predictionSoftmax), key=lambda x:x[1])[0]
		s.vector = predictionSoftmax
		s.name = filename in os.listdir(predictionPath)
		s.genre = genres[predictedIndex]
		lib.songList.append(s.vector)
		lib.labels.append(s.genre)
	
	print (lib.songList)
	print (lib.labels)

	print ("Performing knn")
	dataSet = np.asarray(lib.songList, dtype=np.float32)
	input = lib.songList[0]
	k = 3
	output = kNNclassify(input,dataSet, lib.labels, k)
	
	gbool = raw_input('next: ')

	if gbool == "graph":
		print ("plotting")
		#hyp.plot(dataSet, '.', reduce='TSNE', group=lib.labels, labels=lib.labels, ndims = 3)
		hyp.plot(dataSet, '.', group=lib.labels)
