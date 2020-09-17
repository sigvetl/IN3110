import cv2
import time
from numba import jit
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)

#override to run numba instead of python interpreter
@jit(nopython=True)
def python_color2gray(img):
    """
    creating an empty numpy-array with np.empty with same shape as the image.
    looping over the indexes in the original array and adding the value times the weight
    to the newly created array. casting to uint8 and returning.
    """
    print(img.shape)
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


time1_py = time.time()
grayscale = python_color2gray(image)
grayscale = grayscale.astype("uint8")
cv2.imwrite('rain_grayscale_numba.jpeg', grayscale)
time2_py = time.time()
exec_py = time2_py-time1_py
print(exec_py)

time1_py = time.time()
grayscale = python_color2gray(image)
time2_py = time.time()
exec_py = time2_py-time1_py
print(exec_py)
