import cv2
from numba import jit
import numpy as np


def grayscale_image(input_filename, output_filename=None, scale=None):
    """
    Function is split into main- and helper-function to ensure checking and saving
    of image is possible. These are cheap operations that do not to a significant
    degree influence the running time of the function.
    Checking if input_filename is an array or a file for testing purposes.

    Args:
        input_filename (string): name of image file to be filtered
        output_filename (string): name of filtered image to be saved. If None then filtered image will not be saved
        scale (int): Scale factor to resize image in % of original size. If None then default is 100%

    Returns:
        gray_image (numpy ndarray): 3 dimensional array containing the grayscale pixel values as ints
    """
    if type(input_filename).__module__ == 'numpy':
        image = input_filename
    else:
        image = cv2.imread(input_filename)
    if image is None:
        raise Exception("Not a valid picture")

    if scale != None:
        image = cv2.resize(image, (0,0), fx=(scale/100), fy=(scale/100))
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
