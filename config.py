#Define paths for files
spectrogramsPath = "Data/Spectrograms/"
slicesPath = "Data/Slices/"
datasetPath = "Data/Dataset/"
rawDataPath = "Data/Raw/"
predictionPath = "Predict/Library/"
predictSpect = "Predict/Spectrograms/"
predSlicePath = "Predict/Slices/"

#Spectrogram resolution
pixelPerSecond = 50

#Slice parameters
sliceSize = 128

#Dataset parameters
genreList = {"Pop", "Rap", "Hip-Hop", "Classical", "Rock", "Instrumental", "Jazz", "Electronic", "Punk"}
filesPerGenre = 2000
validationRatio = 0.3
testRatio = 0.1

#Model parameters
batchSize = 128
learningRate = 0.001
nbEpoch = 16