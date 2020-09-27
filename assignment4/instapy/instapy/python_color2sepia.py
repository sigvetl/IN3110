import cv2
import time
import numpy as np

sepia_matrix = [[0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]]

"""
Including check for input filename to ensure there is not created a new array
if the input is already a numpy array. If output_filename is given, saving file.
"""
def sepia_image(input_filename, output_filename=None):
    if type(input_filename).__module__ == 'numpy':
        image = input_filename
    else:
        image = cv2.imread(input_filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    max = 255
    img = np.zeros(image.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            for k in range(img.shape[2]):
                img[i][j][0] += image[i][j][k] * sepia_matrix[0][k]
                img[i][j][1] += image[i][j][k] * sepia_matrix[1][k]
                img[i][j][2] += image[i][j][k] * sepia_matrix[2][k]
            for k in range(img.shape[2]):
                if img[i][j][k] > max:
                    img[i][j][k] = max
    img = img.astype("uint8")
    if output_filename != None:
        cv2.imwrite(output_filename, img)
    return img
