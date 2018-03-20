import csv
import eyed3
import numpy as np
#tag = eyed3.Tag()
#tag.link("/some/file.mp3")
#print tag.getArtist()
#print tag.getTitle()

def getGenre(song):
    file = open('tracks.csv', 'r')
    reader = csv.reader(file)

    header = next(reader)
    header.append(next(reader))
    header = [item for sublist in header for item in sublist] #flattening header
    #next(reader)
    next(reader)
    #data = [row for row in reader] #Read the Remaining Data
    raw = []
    for row in reader:
        raw.append(row)
    
    audiofile = eyed3.load(song)

    search = audiofile.tag.title
    print ("title is ", search)
    found = []

    for sublist in raw:
        #print sublist[52]
        if sublist[52] == search:
            #print sublist
            return sublist[40]

    #print data[0]
    #print type(data)

    #print header
    #print raw
    #print data[0]

    #dataset = dict(zip(header, data.T))

    #print 'track' in dataset
#    return
    


#getGenre('000002.mp3')
