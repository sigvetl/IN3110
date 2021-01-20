import cv2
import time
from numba import jit
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)

#override to run numba instead of python interpreter
#@jit(nopython=True)
def python_color2gray(img):
    """
    creating an empty numpy-array with np.empty with same shape as the image.
    looping over the indexes in the original array and adding the value times the weight
    to the newly created array. casting to uint8 and returning.
    """
    grayscale_img = np.empty(img.shape)
    red = 0.21
    green = 0.72
    blue = 0.07
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            grayscale_img[i][j][0] = img[i][j][0] * blue
            grayscale_img[i][j][1] = img[i][j][1] * green
            grayscale_img[i][j][2] = img[i][j][2] * red
    grayscale_img = grayscale_img.astype("uint8")
    return grayscale_img

def numpy_color2gray(img):
    """
    creating a copy of the image-array. casting it to float.creating a one-dimensional array
    to hold the weights and slicing to mulitply the values with each weight.
    again casting to uint8 and returning.
    """
    grayscale_img = np.copy(img)
    grayscale_img = grayscale_img.astype('float64')
    red = 0.21
    green = 0.72
    blue = 0.07
    rgb = np.array([blue, green, red])
    grayscale_img[:,:,0] *=rgb[0]
    grayscale_img[:,:,1] *=rgb[1]
    grayscale_img[:,:,2] *=rgb[2]
    grayscale_img = grayscale_img.astype("uint8")
    return grayscale_img

time1_py = time.time()
grayscale = python_color2gray(image)
time2_py = time.time()
time1_num = time.time()
grayscale2 = numpy_color2gray(image)
time2_num = time.time()
cv2.imwrite('rain_grayscale2.jpeg', grayscale2)
cv2.imwrite('rain_grayscale.jpeg', grayscale)

exec_py = time2_py-time1_py
exec_num = time2_num-time1_num
print("first run ",exec_py, exec_num)

time1_py = time.time()
grayscale = python_color2gray(image)
time2_py = time.time()
time1_num = time.time()
grayscale2 = numpy_color2gray(image)
time2_num = time.time()
cv2.imwrite('rain_grayscale2.jpeg', grayscale2)
cv2.imwrite('rain_grayscale.jpeg', grayscale)

exec_py = time2_py-time1_py
exec_num = time2_num-time1_num
print("second run ", exec_py, exec_num)

time1_py = time.time()
grayscale = python_color2gray(image)
time2_py = time.time()
time1_num = time.time()
grayscale2 = numpy_color2gray(image)
time2_num = time.time()
cv2.imwrite('rain_grayscale2.jpeg', grayscale2)
cv2.imwrite('rain_grayscale.jpeg', grayscale)

exec_py = time2_py-time1_py
exec_num = time2_num-time1_num
print("third run ",exec_py, exec_num)
