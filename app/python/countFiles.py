import os
from config import slicesPath
dirs = os.listdir('Data/Slices/')

db = []
dirCounts = []
for genre in dirs:
    #sep = '_'
    #Usename = filename.split(sep, 1)[0]
    genreList = os.listdir(slicesPath+genre+'/')
    dirCounts.append(genreList)

print(len(dirCounts))

print(len(db))
#print(len(db))
#genreCounts = []
#for x in genreList:
#    num = db.count(x)
#    genreCounts.append(num)

#count = dict(zip(genreList,genreCounts))

#for key in count:
#    print(key, count[key])

#sortL = sorted(count.items(), key=lambda x: x[1])
#print(sortL)

#genres = []
#genreCounts = []
#for dirs in files:
#   newPath = dirs+'/'
#    genres.append(dirs)
#    for filename in os.listdir(slicesPath+newPath):
#        num = genreCounts.count(filename)
#        genreCounts.append(num)


#print(genres)
#print(genreCounts)
