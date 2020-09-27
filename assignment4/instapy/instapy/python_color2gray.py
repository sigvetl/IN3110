import cv2
import time
import numpy as np

"""
Including check for input filename to ensure there is not created a new array
if the input is already a numpy array. If output_filename is given, saving file.
"""
def grayscale_image(input_filename, output_filename=None):
    if type(input_filename).__module__ == 'numpy':
        image = input_filename
    else:
        image = cv2.imread(input_filename)
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
