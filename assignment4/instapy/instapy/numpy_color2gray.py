import cv2
import numpy as np
from instapy.python_color2gray import grayscale_image as python_gray
from instapy.numba_color2gray import grayscale_image as numba_gray

"""
Main implementation of grayscale_image. Takes an additional argument to determine
which implementation to use. If no argument is given, using numpy.
Checking if input_filename is an array or a file for testing purposes.
Otherwise same functionality as in toGray
"""
def grayscale_image(input_filename, output_filename=None, implementation=None):
    if implementation == 'python':
        py_gray = python_gray(input_filename, output_filename)
        return py_gray
    elif implementation == 'numba':
        numb_gray = numba_gray(input_filename, output_filename)
        return numb_gray
    else:
        if type(input_filename).__module__ == 'numpy':
            image = input_filename
        else:
            image = cv2.imread(input_filename)

        grayscale_img = np.copy(image)
        grayscale_img = grayscale_img.astype('float64')
        red = 0.21
        green = 0.72
        blue = 0.07
        rgb = np.array([blue, green, red])
        grayscale_img[:,:,0] = image.dot(rgb)
        grayscale_img[:,:,1] = image.dot(rgb)
        grayscale_img[:,:,2] = image.dot(rgb)
        grayscale_img = grayscale_img.astype("uint8")

        if output_filename != None:
            cv2.imwrite(output_filename, grayscale_img)
        return grayscale_img
