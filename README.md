# Macaron

Deep Learning Content-Based Music Recommendation.

This model uses a Convolutional Neural Network (CNN) to classify song genres by utilizing image classification on spectrogram
representations of songs. The model would output a N-length vector depicting the predictions for each genre on the song based
on weights loaded from a pretrained model, and use it as input for the k-Nearest Neighbor (kNN) algorithm to produce a playlist of 
k most similar songs in your library directory.

Below are the instructions to run code:

Dependencies:
 - Python 2.7+
 - Sound Exchange (SoX use homebrew to install)
 - Tensorflow (Virtual env)

Python Dependencies:
 - Tflearn
 - Keras
 - Numpy
 - Image


## File Structure:

	/Macaron
		README.md
		/Data
			/Raw
			/Spectrograms
			/Slices
				/Genres		#N directories , N = number of genres to classify
		/Predict
			/Library
			/Spectrograms
			/Slices

## Commands:

### Create Spectrograms and Slices:
(Medium wait time: generate spectrograms for all training data, slicing them and inserting them in their genre folders)
	
	python main.py slice 
	

### Train CNN:
(Long wait time: train over the given epoch length in config file)

	python main.py train


### To classify and/or graph:
(short-medium wait time: predicting song ID vectors, performing kNN, (optional: graph data))

** Wait time depends on number of songs classified in Predict/Library

	python main.py classify
  
(After classification there is a user option to use python package hypertools to generate a 3D 
representation of all classified songs)
	
	input: "graph" to generate, anything else to terminate

### To predict individual song genre:
	
	python main.py predict

