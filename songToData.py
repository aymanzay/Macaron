# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT
import os
from PIL import Image
import eyed3

from sliceSpectrogram import createSlicesFromSpectrograms
from audioFilesTools import isMono
from parsecsv import getGenre
from config import rawDataPath
from config import spectrogramsPath
from config import pixelPerSecond
from config import genreList

import csv

raw = []
file = open('tracks.csv', 'r')

reader = csv.reader(file)
header = next(reader)
next(reader)
next(reader)

for row in reader:
    raw.append(row)


fileGenres = open('genres.csv', 'r')
Greader = csv.reader(fileGenres)

header = next(Greader)
#print(header)
gList = []
for row in Greader:
    gList.append(row)

#Tweakable parameters
desiredSize = 128

#Define
currentPath = os.path.dirname(os.path.realpath(__file__)) 

#Remove logs
eyed3.log.setLevel("ERROR")

#Create spectrogram from mp3 files
def createSpectrogram(filename,newFilename):
        filename = filename.replace("/", "")
        newFilename = newFilename.replace("/", "")

        filename = filename.replace("'", "")
        newFilename = newFilename.replace("'", "")

        #check if already existing
	#if os.path.exists(spectrogramsPath+newFilename):
	#return
        
        #Create temporary mono track if needed
        if isMono(rawDataPath+filename):
                command = "cp '{}' '/tmp/{}.wav'".format(rawDataPath+filename,newFilename)
        else:
                command = "sox '{}' '/tmp/{}.wav' remix 1,2".format(rawDataPath+filename,newFilename)
        p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
        output, errors = p.communicate()
        if errors:
                print (errors)

        #print("TEST")
        #Create spectrogram
        filename.replace(".mp3","")
        command = "sox '/tmp/{}.wav' -n spectrogram -Y 200 -X {} -m -r -o '{}.png'".format(newFilename,pixelPerSecond,spectrogramsPath+newFilename)
        p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, cwd=currentPath)
        output, errors = p.communicate()
        if errors:
                print (errors)

        #Remove tmp mono track
        #try:
                #os.remove("/tmp/{}.wav".format(newFilename))
        #except OSError as exc: # Guard against race condition
        #        if exc.errno != errno.EEXIST:
        #                raise


#Creates .png whole spectrograms from mp3 files
def createSpectrogramsFromAudio():
        genresID = dict()
        files = os.listdir(rawDataPath)
        files = [file for file in files if file.endswith(".mp3")]
        nbFiles = len(files)

        #Create path if not existing
        if not os.path.exists(os.path.dirname(spectrogramsPath)):
                try:
                        os.makedirs(os.path.dirname(spectrogramsPath))
                except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                                raise
        #Rename files according to genre
        for index, filename in enumerate(files):
            print ("Creating spectrogram for file {}/{}...".format(index+1,nbFiles))
            fileGenre = getGenre(raw, gList, rawDataPath+filename)
            print(fileGenre)
            if fileGenre is not None:
                genresID[fileGenre] = genresID[fileGenre] + 1 if fileGenre in genresID else 1
                fileID = genresID[fileGenre]
                if fileID <= 2000:
                    newFilename = str(fileGenre)+"_"+str(fileID)
                    createSpectrogram(filename,newFilename)
                
                
#Whole pipeline .mp3 -> .png slices
def createSlicesFromAudio():
	print ("Creating spectrograms...")
	createSpectrogramsFromAudio()
	print ("Spectrograms created!")

	print ("Creating slices...")
	createSlicesFromSpectrograms(desiredSize)
	print ("Slices created!")
