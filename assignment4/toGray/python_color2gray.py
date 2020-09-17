import cv2
import time
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)

def python_color2gray(img):
    """
    creating an empty numpy-array with np.empty with same shape as the image.
    looping over the indexes in the original array and adding the value times the weight
    to the newly created array. casting to uint8 and storing.
    """
    grayscale_img = np.empty(img.shape)
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
            #grayscale_img[i][j][0] = img[i][j][0] * blue
            #grayscale_img[i][j][1] = img[i][j][1] * green
            #grayscale_img[i][j][2] = img[i][j][2] * red
    grayscale_img = grayscale_img.astype("uint8")
    cv2.imwrite('rain_grayscale_py.jpeg', grayscale_img)

print(image[0])
time1_py = time.time()
grayscale = python_color2gray(image)
time2_py = time.time()

#exec_py = time2_py-time1_py
#print(exec_py)
