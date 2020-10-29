import cv2
import time
import numpy as np

sepia_matrix = [[0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]]


def sepia_image(input_filename, output_filename=None, scale=None):
    """
    creating a zero initialized array to hold the new values with the same size.
    looping through all indicies and assigning the cross product of red, green and blue with the average
    of the first, second and third row of the matrix. when k is initialized for i and j, checking for values above
    255 and setting to max-value if above. casting, writing to file and returning.
    If output_filename is given then saving file.

    Args:
        input_filename (string): name of image file to be filtered
        output_filename (string): name of filtered image to be saved. If None then filtered image will not be saved
        scale (int): Scale factor to resize image in % of original size. If None then default is 100%

    Returns:
        img (numpy ndarray): 3 dimensional array containing the sepia color pixel values as ints
    """

    """
    Including check for input filename to ensure there is not created a new array
    if the input is already a numpy array. If output_filename is given, saving file.
    """
    if type(input_filename).__module__ == 'numpy':
        image = input_filename
    else:
        image = cv2.imread(input_filename)

    if image is None:
        raise Exception("Not a valid picture")

    if scale != None:
        image = cv2.resize(image, (0,0), fx=(scale/100), fy=(scale/100))
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
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if output_filename != None:
        cv2.imwrite(output_filename, img)
    return img
