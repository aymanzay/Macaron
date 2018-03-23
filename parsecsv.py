import csv
import eyed3
import numpy as np

def getGenre(raw, genres, song):

    audiofile = eyed3.load(song)
    search = audiofile.tag.title
    #print ("title is ", search)
    found = ''
    
    for sublist in raw:
        #print sublist[52]
        if sublist[52] == search:
            #print (sublist)
            found = sublist[41]
            break

    temp = ''
    for c in found:
        if c.isdigit():
            temp = temp + c
        elif c == ',':
            break

    #print(temp)
    
    for sublist in genres:
        #print(sublist[0])
        if sublist[0] == temp:
            #print (sublist[3])
            return sublist[3]


