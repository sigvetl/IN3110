import cv2
import time
from numba import jit
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)
if image is None:
    raise Exception("Not a valid picture")


#override to run numba instead of python interpreter
@jit(nopython=True)
def numba_color2gray(img):
#A standard for docstrings is to include information about arguments and return values if there are any
    """
    creating a zeroed numpy-array with np.zeros with same shape as the image.
    looping over the indexes in the original array and adding the value times the average weight
    to the newly created array. casting and writing to file outside of function.

    Args:
        img (numpy ndarray): a 3 dimensional array containing the pixel values of the colored image

    Returns:
        grayscale_img (numpy ndarray): a 3 dimensional array containing the grayscale pixel values as floats
    """
    grayscale_img = np.zeros(img.shape)
    red = 0.21
    green = 0.72
    blue = 0.07
    arr = [blue, green, red]
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                grayscale_img[i][j][0] += img[i][j][k] * arr[k]
                grayscale_img[i][j][1] += img[i][j][k] * arr[k]
                grayscale_img[i][j][2] += img[i][j][k] * arr[k]
    return grayscale_img

#To avoid duplicate code when timing the run time you can have a timing-function
def runtime():
    """
    Times the runtime of the function numba_color2gray including the time it takes to cast the grayscale numpy array values
    to int, and writing to file

    Returns:
        time2_num-time1_num (float): the time taken to run the function
    """
    time1_py = time.time()
    grayscale = numba_color2gray(image)
    grayscale = grayscale.astype("uint8")
    cv2.imwrite('rain_grayscale_numba.jpeg', grayscale)
    time2_py = time.time()
    return time2_py-time1_py

print(runtime())
print(runtime())
print(runtime())
