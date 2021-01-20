#!/usr/bin/env python3
import sys
import cv2
import numpy as np

def ex(list):
    print("hello world")
    print(list)
    print(1)

ex(str(sys.argv))

sepia_matrix = [[0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]]

sepia = np.array(sepia_matrix)

print(sepia[0,:])

def array(*values):
    for i in values:
        print(i)

list = [1, 2, 3]

filename = "rain.jpg"
image = cv2.imread(filename)
gray = image.astype('float64')
rgb = np.array([0.21,0.72,0.07])
product = gray[:,:,0].dot(rgb[0])
cv2.imwrite('example.jpeg', product)
print(product)
print(image[0,0,0])

tuple = (4, 2)
list = [1, 2, 3, 4, 5, 6, 6, 6]
print("h")
print((tuple[0] * tuple[1]) == len(list))
for i in range(tuple[0]):
    print(i)

print(len(list))
for i in range(len(list)):
    print(i)
print("false")
print(False + False +9 + True)
