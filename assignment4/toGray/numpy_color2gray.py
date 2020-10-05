import cv2
import time
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)
if image is None:
    raise Exception("Not a valid picture")


#A standard for docstrings is to include information about arguments and return values if there are any
def numpy_color2gray(img):
    """
    creating a copy of the image-array with numpy.zeros. creating a one-dimensional array
    to hold the weights and slicing to create the dot product of the pixel values and the values with each weight.
    again casting to uint8, writing to file and returning.

    Args:
        img (numpy ndarray): a 3 dimensional array containing the pixel values of the colored image
    """
    grayscale_img = np.zeros(img.shape)
    red = 0.21
    green = 0.72
    blue = 0.07
    bgr = np.array([blue, green, red])
    grayscale_img[:,:,0] = img.dot(bgr)
    grayscale_img[:,:,1] = img.dot(bgr)
    grayscale_img[:,:,2] = img.dot(bgr)
    grayscale_img = grayscale_img.astype("uint8")
    cv2.imwrite('rain_grayscale_num.jpeg', grayscale_img)



#To avoid duplicate code when timing the run time you can have a timing-function
def runtime():
    """
    Times the runtime of the function numpy_color2gray

    Returns:
        time2_num-time1_num (float): the time taken to run the function
    """
    time1_num = time.time()
    grayscale = numpy_color2gray(image)
    time2_num = time.time()
    return time2_num-time1_num

print(runtime())
print(runtime())
print(runtime())
