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

	fileGenre = audiofile.tag.genre


	#No genre
	if not audiofile.tag.genre:
		return None
		#return audiofile.tag.genre.name.encode('utf-8')
	else:
		if("Rock"  in fileGenre):
			fileGenre = "Rock"
		else if("Instrumental"  in fileGenre):
			fileGenre = "Instrumental"
		else if("Piano"  in fileGenre):
			fileGenre = "Classical"
		else if("Jazz"  in fileGenre):
			fileGenre = "Jazz"
		else if("Electronic"  in fileGenre):
			fileGenre = "Electronic"
		else if("Metal"  in fileGenre):
			fileGenre = "Metal"
		else if("Pop"  in fileGenre):
			fileGenre = "Pop"
		else if("Hip-Hop" in fileGenre or "Hip Hop" in fileGenre or "hip hop" in fileGenre):
			fileGenre = "Hip-Hop"

		return fileGenre
