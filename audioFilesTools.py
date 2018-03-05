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
	#audiofile.tag.genre = result #assigning genre tag to song

	fileGenre = audiofile.tag.genre
        

	#No genre
	if not audiofile.tag.genre:
		return None
		#return audiofile.tag.genre.name.encode('utf-8')
	else:
		if("Rock" in str(fileGenre)):
			fileGenre = "Rock"
		if("Instrumental" in str(fileGenre)):
			fileGenre = "Instrumental"
		if("Piano" in str(fileGenre)):
			fileGenre = "Classical"
		if("Jazz" in str(fileGenre)):
			fileGenre = "Jazz"
		if("Electronic" in str(fileGenre)):
			fileGenre = "Electronic"
		if("Metal" in str(fileGenre)):
			fileGenre = "Metal"
		if("Pop" in str(fileGenre)):
			fileGenre = "Pop"
		if("Hip-Hop" in str(fileGenre) or "Hip Hop" in str(fileGenre) or "hip hop" in str(fileGenre)):
			fileGenre = "Hip-Hop"

		return fileGenre
