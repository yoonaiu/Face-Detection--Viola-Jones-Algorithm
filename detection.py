import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from PIL import Image, ImageOps
import re
import glob
import utils
import numpy as np

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")

    """
    function detail:
      1. load the image base on the content in detectData.txt.
         first store the information: (img_name, ori_img, number_of_faces, face_info*number_of_faces) to info
         type:
            info: list of (img_name, ori_img, number_of_faces, face_info*number_of_faces) tuple
            img_name: string
            ori_img:  nparray with shape m*n*1  [discarded, no-use]
            number_of_faces: int
            face_info: list of string(represent number info),
                       face_info[0]: the left up point's x(colum) value of the range
                       face_info[1]: the left up point's y(row) value of the range
                       face_info[2]: the x length of the range
                       face_info[3]: the y length of the range

      2. every time if the first word is *.jpg, it means that start a new image info
         , otherwise, keep append the face_info to the current info[k]

      3. append thing to tuple: info[cnt] += (word_list,) 
         -> (X,) need to use "," to represent this is a tuple, or (X) would be list
    """
    # load the image base on the content in detectData.txt
    # first load the whole image, and than crop the part of the nparray out of the original one
    f = open(dataPath, 'r')  # 'data/detect/detectData.txt'

    info = []
    cnt = -1
    for line in f.readlines():
      word_list = line.split()
      # if re.match(r'[\w.-]z+.jpg', word_list[0] ):
      leng = len(word_list[0])
      #print(leng)
      #print( word_list[0] )
      # print( type(word_list[0]) )
      if leng > 4 and word_list[0][leng-3: leng] == "jpg":
        # print("a")
        img_name = word_list[0]
        # ori_img = ( cv2.imread( glob.glob('data/detect/'+ word_list[0] ), cv2.IMREAD_GRAYSCALE ) ) -> don't need glob glob
        ori_img = ( cv2.imread( 'data/detect/' + word_list[0], cv2.IMREAD_GRAYSCALE ) )
        info.append( (img_name, ori_img, word_list[1]) )
        cnt += 1
      else:  # the info of face
        #info[cnt] += int(word_list)
        info[cnt] += (word_list,) # add list to original tuple

    """
    function detail:
      1. use the img_name stored in info to open the corresponding img in the file
         * don't need to use glob.glob here, cuz we can directly pass in the "known path" of certain img file

      2. get the sub_img - use pillow PIL
         (1) open the img by name
         (2) crop the sub_img from the original img
         (3) turn the sub_img to grayscale
         (4) resize the sub_img to 19x19
         (5) turn the sub_img into numpy array
      
      3. put the numpy array,sub_img_arr, into clf.classify() to determine face or non-face

      4. draw the box base on the result from the clf.classify()
         How to draw a box?
            (1) open the img: im = Image.open( 'data/detect/' + img_info[0] )
            (2) let plt to draw on im:  plt.imshow(im)
            (3) get the axes from the plt: ax = plt.gca()
            (4) use "Rectangle" to specify the box with traits we want: 
                rect = Rectangle((col, row), col_scale, row_scale, linewidth=1,edgecolor='g',facecolor='none')
            (5) add the rectangle to axes throughout the process: ax.add_patch(rect)
            (6) show the plt at the end: plt.show()
    
    nothing to return, just show the result
    """

    for img_info in info:
      im = Image.open( 'data/detect/' + img_info[0] )
      plt.imshow(im)
      ax = plt.gca()

      ori_img = img_info[1]
      face_num = int(img_info[2])
      for i in range( face_num ):  # face info: 3~3+i
        row = int(img_info[3+i][1]) # x, y -> up left point
        col = int(img_info[3+i][0])
        row_scale = int(img_info[3+i][3]) # !=  img_info[3+i][3]
        col_scale = int(img_info[3+i][2])
        # sub_img = ori_img[row:row+row_scale, col:col+col_scale]
        sub_img = im.crop((col, row, col+col_scale, row+row_scale))  # left top right bottom
        sub_img = ImageOps.grayscale( sub_img )
        sub_img = sub_img.resize((19, 19))
        sub_img_arr = np.array( sub_img )
        # sub_img = utils.integralImage(sub_img)
        # sub_img = ori_img[row-scale:row, col:col+scale]
        face = clf.classify( sub_img_arr )
        if face == 1:
          rect = Rectangle((col, row), col_scale, row_scale, linewidth=1,edgecolor='g',facecolor='none') # up left
          ax.add_patch(rect)
        else:
          rect = Rectangle((col, row), col_scale, row_scale, linewidth=1,edgecolor='r',facecolor='none')
          ax.add_patch(rect)

      plt.show()

    # End your code (Part 4)

    '''
    # ori_img = []
    ori_img = ()  # empty nparray
    img_id_now = -1 # seems like no use
    face_num = 0 # seems like no use
    img_name_now = ""
    im, ax

    for line in f.readlines():
      word_list = line.split()
      if re.match( "*.jpg", word_list[0] ):
        ori_img = ( cv2.imread( glob.glob('data/detect/'+ word_list[0] ), cv2.IMREAD_GRAYSCALE ) )
        img_id_now += 1
        face_num = word_list[1]


        img_name_now = word_list[0]
        im = Image.open( img_name_now )
        plt.imshow(im)
        ax = im.gca
      
      # if not the line with jpg, use the ith face know that to which face we are processing with with the face_cnt
      # wordlist[0] -> col to start with
      # wordlist[1] -> row to start with
      # wordlist[2, 3] -> the expend range
      # process the sub_image and draw the box
      sub_image = ori_img[ wordlist[1]:wordlist[1]+wordlist[2], wordlist[0]:wordlist[0]+wordlist[3] ]
      face = clf.classify( sub_image )

      # draw a box on the image
      
      if face == 1:
        rect = Rectangle((wordlist[0],wordlist[1]),wordlist[2],wordlist[3],linewidth=1,edgecolor='g',facecolor='none') # bottom left
        ax.add_patch(rect)
      else:
        rect = Rectangle((wordlist[0],wordlist[1]),wordlist[2],wordlist[3],linewidth=1,edgecolor='r',facecolor='none')
        ax.add_patch(rect)
    '''
