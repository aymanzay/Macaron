# -*- coding: utf-8 -*-
import eyed3
from config import genreList

#Remove logs
eyed3.log.setLevel("ERROR")

def isMono(filename):
	audiofile = eyed3.load(filename)
	return audiofile.info.mode == 'Mono'

def getGenre(filename):

	audiofile = eyed3.load(filename)
	test = filename.replace(".mp3","")
	test = test.replace("_", "")
	test = test.replace("Data/Raw/", "")
	result = u''.join([i for i in test if not i.isdigit()]) #return string with no directory path or song number
	print result
	
	#audiofile.tag.genre = result #assigning genre tag to song

	fileGenre = audiofile.tag.genre.name

	for n in genreList:
		if n in fileGenre:
			return n
		
	if "Piano" in fileGenre:
		return genreList[3]

	if "hip hop" in fileGenre or "Hip Hop" in fileGenre:
		return genreList[2]

	if None:
		fileGenre = "x"
		return fileGenre
	else:
		fileGenre = "x"
		return fileGenre

	#check if fileGenre is in/related to any of list items then return the corresponding genre
	
	#No genre
	#if not audiofile.tag.genre:
	#	return None
		#return audiofile.tag.genre.name.encode('utf-8')
	#else:
	#	return fileGenre
