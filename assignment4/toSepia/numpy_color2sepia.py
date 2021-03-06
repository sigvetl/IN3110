import cv2
import time
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)
if image is None:
    raise Exception("Not a valid picture")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
sepia_matrix = [[0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]]
sepia = np.array(sepia_matrix)


def numpy_color2sepia(image, matrix):
# A standard for docstrings is to include information about arguments and return values if there are any
    """
    creating a zero initialized copy of the image-array. filling the array with the cross product
    of the red, green and blue values of the image and the first second and third row of the matrix.
    clipping the array to a max value of 255 where the values are higher. casting, writing to file and returning.

    Args:
        image (numpy ndarray): a 3 dimensional array containing the pixel values of the colored image
        matrix (numpy ndarray): a 2 dimensional array containing the sepia color weights

    Returns:
        img (numpy ndarray): a 3 dimensional array containing the sepia color pixel values
    """
    img = np.zeros(image.shape)
    img[:,:,0] = image.dot(matrix[0,:])
    img[:,:,1] = image.dot(matrix[1,:])
    img[:,:,2] = image.dot(matrix[2,:])
    img = np.clip(img, 0, 255)
    img = img.astype("uint8")
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite('rain_sepia_num.jpeg', img)
    return img



#To avoid duplicate code when timing the run time you can have a timing-function
def runtime():
    """
    Times the runtime of the function python_color2sepia including the time it takes to cast the grayscale numpy array values
    to int, and writing to file

    Returns:
        time2_num-time1_num (float): the time taken to run the function
    """
    time1_num = time.time()
    sepia_img = numpy_color2sepia(image, sepia)
    time2_num = time.time()
    return time2_num-time1_num

print(runtime())
print(runtime())
print(runtime())
