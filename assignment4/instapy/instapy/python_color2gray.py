import cv2
import time
import numpy as np


def grayscale_image(input_filename, output_filename=None, scale=None):
    """
    creating an empty numpy-array with np.zeros with same shape as the image.
    If scale given then resizing to % given.
    looping over the indexes in the original array and adding the value times the weight
    to the newly created array. casting to uint8 and storing. time-tracking using time.time().
    If output_filename is given then saving file.

    Args:
        input_filename (string): name of image file to be filtered
        output_filename (string): name of filtered image to be saved. If None then filtered image will not be saved
        scale (int): Scale factor to resize image in % of original size. If None then default is 100%

    Returns:
        grayscale_img (numpy ndarray): 3 dimensional array containing the grayscale pixel values as ints
    """

    """
    Including check for input filename to ensure there is not created a new array
    if the input is already a numpy array.
    """
    if type(input_filename).__module__ == 'numpy':
        image = input_filename
    else:
        image = cv2.imread(input_filename)

    if image is None:
        raise Exception("Not a valid picture")

    if scale != None:
        image = cv2.resize(image, (0,0), fx=(scale/100), fy=(scale/100))
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
    grayscale_img = grayscale_img.astype("uint8")
    if output_filename != None:
        cv2.imwrite(output_filename, grayscale_img)
    return grayscale_img
