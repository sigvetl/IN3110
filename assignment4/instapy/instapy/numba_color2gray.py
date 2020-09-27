import cv2
from numba import jit
import numpy as np

"""
Function is split into main- and helper-function to ensure checking and saving
of image is possible. These are cheap operations that does not to a significant
degree influence the running time of the function.
"""
def grayscale_image(input_filename, output_filename=None):
    if type(input_filename).__module__ == 'numpy':
        image = input_filename
    else:
        image = cv2.imread(input_filename)
    gray_image = numba_color2gray(image)
    gray_image = gray_image.astype("uint8")
    if output_filename != None:
        cv2.imwrite(output_filename, gray_image)
    return gray_image

#override to run numba instead of python interpreter
@jit(nopython=True)
def numba_color2gray(image):
    grayscale_img = np.zeros(image.shape)
    red = 0.21
    green = 0.72
    blue = 0.07
    arr = [blue, green, red]
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                grayscale_img[i][j][0] += image[i][j][k] * arr[k]
                grayscale_img[i][j][1] += image[i][j][k] * arr[k]
                grayscale_img[i][j][2] += image[i][j][k] * arr[k]
    return grayscale_img
