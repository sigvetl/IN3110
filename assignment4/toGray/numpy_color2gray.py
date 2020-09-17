import cv2
import time
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)

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
    grayscale_img[:,:,0] = img.dot(rgb)
    grayscale_img[:,:,1] = img.dot(rgb)
    grayscale_img[:,:,2] = img.dot(rgb)
    grayscale_img = grayscale_img.astype("uint8")
    cv2.imwrite('rain_grayscale_num.jpeg', grayscale_img)

time1_num = time.time()
grayscale = numpy_color2gray(image)
time2_num = time.time()

exec_num = time2_num-time1_num
print(exec_num)
