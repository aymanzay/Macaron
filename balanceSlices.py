import os
from config import slicesPath
from config import setBalance
files = os.listdir(slicesPath)

#TODO: change os.remove to move slices to new directory for possible later testing.
for genre in files:
    newPath = slicesPath+genre+'/'
    i = 0
    for filename in os.listdir(newPath):
        if i < (setBalance*11):
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
    
