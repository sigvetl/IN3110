import cv2
import time
from numba import jit
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)
if image is None:
    raise Exception("Not a valid picture")
#cv2 is BGR - the matrix is RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
matrise = np.array([[0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]])

"""
creating a zero initialized array to hold the new values with the same size.
looping through all indicies and assigning the cross product of red, green and blue with the average
of the first, second and third row of the matrix. when k is initialized for i and j, checking for values above
255 and setting to max-value if above. returning. casting and writing to file outside of function.
"""
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

time1_py = time.time()
sepia_img = color2sepia(image, matrise)
sepia_img = sepia_img.astype("uint8")
sepia_img = cv2.cvtColor(sepia_img, cv2.COLOR_RGB2BGR)
cv2.imwrite('rain_sepia_numba.jpeg', sepia_img)
time2_py = time.time()
exec = time2_py-time1_py
print(exec)

time1_py = time.time()
sepia_img = color2sepia(image, matrise)
sepia_img = sepia_img.astype("uint8")
sepia_img = cv2.cvtColor(sepia_img, cv2.COLOR_RGB2BGR)
cv2.imwrite('rain_sepia_numba.jpeg', sepia_img)
time2_py = time.time()
exec = time2_py-time1_py
print(exec)

time1_py = time.time()
sepia_img = color2sepia(image, matrise)
sepia_img = sepia_img.astype("uint8")
sepia_img = cv2.cvtColor(sepia_img, cv2.COLOR_RGB2BGR)
cv2.imwrite('rain_sepia_numba.jpeg', sepia_img)
time2_py = time.time()
exec = time2_py-time1_py
print(exec)
