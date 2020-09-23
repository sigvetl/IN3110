import cv2
import time
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
sepia_matrix = [[0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]]
sepia = np.array(sepia_matrix)

"""
creating a zero initialized copy of the image-array. filling the array with the cross product
of the red, green and blue values of the image and the first second and third row of the matrix.
clipping the array to a max value of 255 where the values are higher. casting, writing to file and returning.
"""
def numpy_color2sepia(image, matrix):
    img = np.zeros(image.shape)
    img[:,:,0] = image.dot(matrix[0,:])
    img[:,:,1] = image.dot(matrix[1,:])
    img[:,:,2] = image.dot(matrix[2,:])
    img = np.clip(img, 0, 255)
    img = img.astype("uint8")
    cv2.imwrite('rain_sepia_num.jpeg', img)
    return img

time1_num = time.time()
sepia_img = numpy_color2sepia(image, sepia)
time2_num = time.time()
exec_num = time2_num-time1_num
print(exec_num)

time1_num = time.time()
sepia_img = numpy_color2sepia(image, sepia)
time2_num = time.time()
exec_num = time2_num-time1_num
print(exec_num)

time1_num = time.time()
sepia_img = numpy_color2sepia(image, sepia)
time2_num = time.time()
exec_num = time2_num-time1_num
print(exec_num)
