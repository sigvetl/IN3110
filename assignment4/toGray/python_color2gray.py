import cv2
import time
import numpy as np

filename = "rain.jpg"
image = cv2.imread(filename)
if image is None:
    raise Exception("Not a valid picture")


# A standard for docstrings is to have it as the first thing in the function,
# and include information about argument(s) and return value(s) if there are any
def python_color2gray(img):
    """
    creating an empty numpy-array with np.zeros with same shape as the image.
    looping over the indexes in the original array and adding the value times the weight
    to the newly created array. casting to uint8 and storing. time-tracking using time.time().

    Args:
        img (numpy ndarray): a 3 dimensional array containing the pixel values of the colored image
    """
    grayscale_img = np.zeros(img.shape)
    red = 0.21
    green = 0.72
    blue = 0.07
    # Instead of having 3 for-loops you could have 2 for-loops, making the implementation faster and the code slightly easier to understand
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            grayscale_img[i][j] = img[i][j][0]*blue + img[i][j][1]*green + img[i][j][2]*red
    #arr = [blue, green, red]
    # for i in range(img.shape[0]):
    #     for j in range(img.shape[1]):
    #         for k in range(img.shape[2]):
    #             grayscale_img[i][j][0] += img[i][j][k] * arr[k]
    #             grayscale_img[i][j][1] += img[i][j][k] * arr[k]
    #             grayscale_img[i][j][2] += img[i][j][k] * arr[k]
    grayscale_img = grayscale_img.astype("uint8")
    cv2.imwrite('rain_grayscale_py.jpeg', grayscale_img)


#To avoid duplicate code when timing the run time you can have a timing-function
def runtime():
    """
    Times the runtime of the function python_color2gray

    Returns:
        time2_py-time1_py (float): the time taken to run the function
    """
    time1_py = time.time()
    grayscale = python_color2gray(image)
    time2_py = time.time()
    return time2_py-time1_py

print(runtime())
# print(runtime())
# print(runtime())
