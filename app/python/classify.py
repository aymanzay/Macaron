import random
import string
import os
import sys
import glob
import numpy as np
import tensorflow as tf
from PIL import Image
from pathlib import Path
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

currentPath = os.path.dirname(os.path.realpath(__file__)) 
s = song()
lib = library()

def classify():
    #List genres
    genres = os.listdir(slicesPath)
    genres = [filename for filename in genres if os.path.isdir(slicesPath+filename)]
    nbClasses = len(genres)

    #Create model
    model = createModel(nbClasses, sliceSize)
    #s = song()
    #lib = library()

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

    #print ("Creating Spectrogams")
    #parse through all files in library and create spectrograms
    for filename in os.listdir(predictionPath):
        if filename.endswith(".mp3"):
            newFilename = 'new_' + filename
            newFilename = newFilename.replace(".mp3", "")

            if (Path(predictSpect+newFilename)).exists():
                break
            
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
            #os.remove("/tmp/{}.wav".format(newFilename))
            counter += 1

    subdata = []
    data = []

    #print ("Spectrogams Created! ")
    #slice spectrograms

    #print ("Slicing Spectrogams")
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


    #print ("Slices Created! ")

    model.load('python/musicDNN.tflearn')
    #print ("Model loaded! ")

    #print data

    #parse through super array predicting each one 
    #and assign name to song object then append song object to songList in library
    #print ("Predicting")
    for vec in data:
        predictionSoftmax = model.predict(vec)[0]
        predictedIndex = max(enumerate(predictionSoftmax), key=lambda x:x[1])[0]
        s.vector = predictionSoftmax
        s.name = filename in os.listdir(predictionPath)
        s.genre = genres[predictedIndex]
        lib.songList.append(s.vector)
        lib.labels.append(s.genre)
    

    for x in lib.songList:
        print x

#List genres
genres = os.listdir(slicesPath)
genres = [filename for filename in genres if os.path.isdir(slicesPath+filename)]
nbClasses = len(genres)

#Create model
model = createModel(nbClasses, sliceSize)
    

def test_classify():

    #initial check to see if an arrays.txt file already exists and matches songs in the library
    if (os.path.is_file("arrays.txt")):

    
    subdata = []
    data = []

    #print ("Spectrogams Created! ")
    for newFilename in os.listdir(predictSpect):
        if newFilename.endswith(".png"):
            #slice
            img = Image.open(predictSpect+newFilename)

            width, height = img.size
            nbSamples = int(width/sliceSize)
            width - sliceSize

            #For each sample
            for i in range(nbSamples):
                img_array = getImageData(predSlicePath+newFilename[:-4]+"_"+str(i)+".png", sliceSize)
                subdata.append(img_array)
        data.append(subdata)
        subdata = []
    #print ("Slices Created! ")

    model.load('python/musicDNN.tflearn')
    #print ("Model loaded! ")

    #print data

    #parse through super array predicting each one 
    #and assign name to song object then append song object to songList in library
    #print ("Predicting")
    for vec in data:
        predictionSoftmax = model.predict(vec)[0]
        predictedIndex = max(enumerate(predictionSoftmax), key=lambda x:x[1])[0]
        s.vector = predictionSoftmax
        s.name = filename in os.listdir(predictionPath)
        s.genre = genres[predictedIndex]
        lib.songList.append(s.vector)
        lib.labels.append(s.genre)
    

    out = open('arrays.txt', 'w')
    for x in lib.songList:
        out.write("%s\n" % x)
    

def knnRequest(index):
    #model.load('python/musicDNN.tflearn')
    file_content = open('middle.txt')
    counter = 0
    arrays = []
    for line in file_content:
        arrays = line.split(",")

    data = []
    temp = []
    for vec in arrays:
        temp.append(vec)
        counter = counter + 1
        if counter == 8:
            data.append(temp)
            temp = []
            counter = 0
    
    for vec in data:
        maxV = np.argmax(vec)
        sGenre = genres[maxV]
        lib.labels.append(sGenre)

    #print lib.labels

    dataSet = np.asarray(data, dtype=np.float32)
    inputS = dataSet[0]
    k = 20
    output = kNNclassify(inputS, dataSet, lib.labels, k)
    
    out = open('translated.txt', 'w')
    for item in output:
        print item
        out.write("%s\n" % item)


if "classify" in sys.argv[1]:
    test_classify()

if "generate" in sys.argv[1]:
    index = sys.argv[2]
    knnRequest(index)

