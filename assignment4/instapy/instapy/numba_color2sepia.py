import cv2
import time
from numba import jit
import numpy as np

matrise = np.array([[0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]])


def sepia_image(input_filename, output_filename=None, scale=None):
    """
    Function is split into main- and helper-function to ensure checking and saving
    of image is possible. These are cheap operations that does not to a significant
    degree influence the running time of the function.
    Checking if input_filename is an array or a file for testing purposes.

    Args:
        input_filename (string): name of image file to be filtered
        output_filename (string): name of filtered image to be saved. If None then filtered image will not be saved
        scale (int): Scale factor to resize image in % of original size. If None then default is 100%

    Returns:
        sepia_img (numpy ndarray): 3 dimensional array containing the sepia color pixel values as ints
    """
    if type(input_filename).__module__ == 'numpy':
        image = input_filename
    else:
        image = cv2.imread(input_filename)
    if image is None:
        raise Exception("Not a valid picture")

    if scale != None:
        image = cv2.resize(image, (0,0), fx=(scale/100), fy=(scale/100))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    sepia_image = color2sepia(image, matrise)
    sepia_image = sepia_image.astype("uint8")
    sepia_image = cv2.cvtColor(sepia_image, cv2.COLOR_RGB2BGR)
    if output_filename != None:
        cv2.imwrite(output_filename, sepia_image)
    return sepia_image

@jit(nopython=True)
def color2sepia(image, matrix):
    max = 255
    img = np.zeros(image.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                img[i][j][0] += image[i][j][k] * matrix[0][k]
                img[i][j][1] += image[i][j][k] * matrix[1][k]
                img[i][j][2] += image[i][j][k] * matrix[2][k]
            for k in range(img.shape[2]):
                if img[i][j][k] > max:
                    img[i][j][k] = max
    return img
