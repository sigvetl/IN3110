import cv2
import time
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)

#cv2 is BGR - the matrix is RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
sepia_matrix = [[0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]]

def color2sepia(image, sepia_matrix):
    max = 255
    img = np.zeros(image.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                img[i][j][0] += image[i][j][k] * sepia_matrix[0][k]
                img[i][j][1] += image[i][j][k] * sepia_matrix[1][k]
                img[i][j][2] += image[i][j][k] * sepia_matrix[2][k]
            for k in range(img.shape[2]):
                if img[i][j][k] > 255:
                    img[i][j][k] = 255
    img = img.astype("uint8")
    cv2.imwrite('rain_sepia_py_test.jpeg', img)

time1_py = time.time()
sepia = color2sepia(image, sepia_matrix)
time2_py = time.time()

exec = time2_py-time1_py
print(exec)
