import cv2
import numpy as np
from instapy.python_color2sepia import sepia_image as python_sepia
from instapy.numba_color2sepia import sepia_image as numba_sepia

"""
Main implementation of sepia_image. Takes an additional argument to determine
which implementation to use. If no argument is given, using numpy.
Checking if input_filename is an array or a file for testing purposes.
Otherwise same functionality as in toSepia
"""
def sepia_image(input_filename, output_filename=None, implementation=None, scale=None):
    if implementation == 'python':
        py_sep = python_sepia(input_filename, output_filename, scale)
        return py_sep
    elif implementation == 'numba':
        numb_sep = numba_sepia(input_filename, output_filename, scale)
        return numb_sep
    else:
        sepia = np.array([[0.393, 0.769, 0.189],
                        [0.349, 0.686, 0.168],
                        [0.272, 0.534, 0.131]])
        if type(input_filename).__module__ == 'numpy':
            image = input_filename
        else:
            image = cv2.imread(input_filename)
        if image is None:
            raise Exception("Not a valid picture")

        if scale != None:
            image = cv2.resize(image, (0,0), fx=(scale/100), fy=(scale/100))

        #ERROR CHECK
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        img = np.zeros(image.shape)
        img[:,:,0] = image.dot(sepia[0,:])
        img[:,:,1] = image.dot(sepia[1,:])
        img[:,:,2] = image.dot(sepia[2,:])
        img = np.clip(img, 0, 255)
        img = img.astype("uint8")
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if output_filename != None:
            cv2.imwrite(output_filename, img)
        return img
