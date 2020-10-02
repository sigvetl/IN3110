from instapy.numpy_color2gray import grayscale_image as gray
from instapy.numpy_color2sepia import sepia_image as sepia
import numpy as np
import random as r
import cv2

#creating a random pixel picture
testarr = np.random.randint(0,255,(400, 600, 3))

sepia_matrix = np.array([[0.393, 0.769, 0.189],
                         [0.349, 0.686, 0.168],
                         [0.272, 0.534, 0.131]])
gray_matrix = np.array([0.07, 0.72, 0.21])

#saving the random picture as testarr.jpg
cv2.imwrite('testarr.jpg', testarr)
image = cv2.imread('testarr.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

"""
Testing function that ensures that all implementations correctly
transforms pixels by creating a hardcoded random pixel and testing against
the same pixel in the returned array from all implementations.
"""
def test_sepia_pixel():
    pixel = np.zeros(3)
    python_sepia_image = sepia('testarr.jpg', 'instapy_sepia_py.jpg', 'python')
    numba_sepia_image = sepia('testarr.jpg', 'instapy_sepia_numba.jpg', 'numba')
    sepia_image = sepia('testarr.jpg', 'instapy_sepia_numpy.jpg')
    pixel[0] = image[255,590,:].dot(sepia_matrix[0,:])
    pixel[1] = image[255,590,:].dot(sepia_matrix[1,:])
    pixel[2] = image[255,590,:].dot(sepia_matrix[2,:])
    pixel = np.clip(pixel, 0, 255)
    pixel = pixel.astype("uint8")
    #flipping the image back
    temp = pixel[0]
    pixel[0] = pixel[2]
    pixel[2] = temp
    assert np.all(pixel == sepia_image[255,590,:])
    assert np.all(pixel == numba_sepia_image[255,590,:])
    assert np.all(pixel == python_sepia_image[255,590,:])

"""
Testing that the shape of the returned image is the same as the shape of the random array
"""
def test_shape():
    gray_image = gray('testarr.jpg')
    sepia_image = sepia('testarr.jpg')
    assert gray_image.shape == testarr.shape
    assert sepia_image.shape == testarr.shape

"""
Testing function that ensures that all implementations correctly
transforms pixels by creating a hardcoded random pixel and testing against
the same pixel in the returned array from all implementations.
"""
def test_gray_pixel():
    numpy_gray_image = gray(testarr, 'test_instapy_numpy.jpg')
    python_gray_image = gray(testarr, 'test_instapy_py.jpg', 'python')
    numba_gray_image = gray(testarr, 'test_instapy_numba.jpg', 'numba')
    pixel = np.zeros(3)
    pixel[:] = testarr[256,488,:].dot(gray_matrix)
    pixel = pixel.astype("uint8")
    assert np.all(numpy_gray_image[256,488,:] == pixel)
    assert np.all(python_gray_image[256,488,:] == pixel)
    assert np.all(numba_gray_image[256,488,:] == pixel)
