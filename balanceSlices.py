import os
from config import slicesPath

files = os.listdir(slicesPath)

for genre in files:
    newPath = slicesPath+genre+'/'
    i = 0
    for filename in os.listdir(newPath):
        if i < (1000*11):
            newNametup = filename.split('_')
            names = newNametup[0]
        else:
            if not os.path.exists(os.path.dirname('Data/ExtraData/')):
                try:
                        os.makedirs(os.path.dirname('Data/ExtraData/'))
                except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                                raise
            os.remove(newPath+filename)
        i = i + 1
    
