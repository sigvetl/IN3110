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

def numpy_color2sepia(image, matrix):
    """
    creating a copy of the image-array. casting it to float.creating a one-dimensional array
    to hold the weights and slicing to mulitply the values with each weight.
    again casting to uint8 and returning.
    """
    img = np.zeros(image.shape)
    #img = img.astype('float64')
    img[:,:,0] = image.dot(matrix[0,:])
    img[:,:,1] = image.dot(matrix[1,:])
    img[:,:,2] = image.dot(matrix[2,:])
    #print("image",image.dot(matrix[0,0]))
    img = np.clip(img, 0, 255)
    img = img.astype("uint8")
    cv2.imwrite('rain_sepia_num.jpeg', img)

time1_num = time.time()
sepia = numpy_color2sepia(image, sepia)
time2_num = time.time()

exec_num = time2_num-time1_num
print(exec_num)