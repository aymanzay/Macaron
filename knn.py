#coding:utf-8

from numpy import *
import operator
from array import array

###Sorting by KNN
def kNNclassify(input,dataSet,label,k):
    dataSize = dataSet.shape[0]

    #Calculate euclidean distance
    diff = tile(input,(dataSize,1)) - dataSet

    sqdiff = diff ** 2
    
    #Adding row vector respectively and then get new row vector. 
    squareDist = sum(sqdiff,axis = 1)
    dist = squareDist ** 0.5
    
    #Sorting the distance
    #Sorting based on the value of elements(greater -> less), return subscript
    sortedDistIndex = argsort(dist)
    songList = []

    #append top k most similar to list
    for i in range(0, k):
        index = sortedDistIndex[i]
        songList.append([label[index],dataSet[index]])

    return songList
