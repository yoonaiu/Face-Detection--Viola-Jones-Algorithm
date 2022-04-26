import os
import cv2
import glob

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")

    """
    function detail:
      1. use glob.glob( given_path ) to catch all the filename under given path layer
         use *.pgm to represent all files' names
      2. dataset is a list, so use "append" to add element to it, and use [] to initialize it

    Returns:
      dataset: (numpy_array, label)
        numpy_array:  image content, only m*n*1, so need to store it as grayscale;
                      if store as color, its shape will be m*n*3(RGB)
        label:        face 1, non-face 0
    """
    # cnt = 0
    dataset = []
    for img in glob.glob(dataPath + '/face/*.pgm') :
      dataset.append( (cv2.imread(img, cv2.IMREAD_GRAYSCALE), 1) )
      #if cnt == 0:
        #print( cv2.imread(img, cv2.IMREAD_GRAYSCALE).shape )
        #cnt = 1
    
    for img in glob.glob(dataPath + '/non-face/*.pgm') :
      dataset.append( (cv2.imread(img, cv2.IMREAD_GRAYSCALE), 0) )

    # End your code (Part 1)
    return dataset
