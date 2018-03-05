# -*- coding: utf-8 -*-
import eyed3

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
	audiofile.tag.genre = result #assigning genre tag to song

	fileGenre = audiofile.tag.genre.name


	#No genre
	if not audiofile.tag.genre:
		return None
		#return audiofile.tag.genre.name.encode('utf-8')
	else:
		if("Rock" in fileGenre):
			fileGenre = "Rock"
		if("Instrumental" in fileGenre):
			fileGenre = "Instrumental"
		if("Piano" in fileGenre):
			fileGenre = "Classical"
		if("Jazz" in fileGenre):
			fileGenre = "Jazz"
		if("Electronic" in fileGenre):
			fileGenre = "Electronic"
		if("Metal" in fileGenre):
			fileGenre = "Metal"
		if("Pop" in fileGenre):
			fileGenre = "Pop"
		if("Hip-Hop" in fileGenre or "Hip Hop" in fileGenre or "hip hop" in fileGenre):
			fileGenre = "Hip-Hop"

		return fileGenre.encode('utf-8')
