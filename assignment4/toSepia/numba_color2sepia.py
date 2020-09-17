import cv2
import time
from numba import jit
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)

#cv2 is BGR - the matrix is RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
matrise = np.array([[0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]])

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
                if img[i][j][k] > 255:
                    img[i][j][k] = 255
    return img
    img = img.astype("uint8")
    cv2.imwrite('rain_sepia_py_test.jpeg', img)

time1_py = time.time()
sepia = color2sepia(image, matrise)
print(sepia[200,250,0])
print(sepia[207][300])
sepia = sepia.astype("uint8")
print(sepia[200,300:305,:])
cv2.imwrite('rain_sepia_numba.jpeg', sepia)
time2_py = time.time()

exec = time2_py-time1_py
print(exec)
