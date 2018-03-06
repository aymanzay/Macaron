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


File Structure:
/Macaron
    /Predict
      /Library
      /Slices
      /Spectrograms
    /Data
        /Raw
        /Spectrograms
        /Slices
          /(list of genres to classify) 

Commands:

Create Spectrogram and Slice pngs:
  python main.py slice

(wait for it to generate spectrograms and slices into their genre folders)

Train CNN:
  python main.py train

(It will train over the given epoch length in config file)

To classify or graph:
  python main.py classify
  
(After classification there is a user option to use python package hypertools to generate a 3D 
representation of all classified songs)
input: "graph" to generate, anything else to terminate

To predict individual song genre:
python main.py predict

