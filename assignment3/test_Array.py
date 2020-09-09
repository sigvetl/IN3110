#!/usr/bin/env python3

from Array import Array

#print-test
def test_print(array, array2):
    assert array.__str__() == "[1, 2, 3, 4]"
    assert array2.__str__() == "[2, 4, 6, 8]"

#tests for adding element to array
def test_add_element(array, other, number):
    assert array.__add__(other) == [6, 7, 8, 9]
    assert array.__add__(number) == [4, 5, 6, 7]

#tests for adding array to array
def test_add_array(array, other, fail):
    assert array.__add__(other) == [3, 6, 9, 12]
    assert array.__add__(fail) == "NotImplemented"

def test_add_element_2d(array, other):
    #assert
    pass

#tests for subtracting element from array
def test_sub_element(array, other, number):
    assert array.__sub__(otherElement) == [-4, -3, -2, -1]
    assert array.__sub__(number) == [-2, -1, 0, 1]

#tests for subtracting array from array
def test_sub_array(array, other, fail):
    assert array.__sub__(other) == [-1, -2, -3, -4]
    assert array.__sub__(fail) == "NotImplemented"

#tests for multiplying element with array
def test_mul_element(array, other, number):
    assert array.__mul__(other) == [5, 10, 15, 20]
    assert array.__mul__(number) == [3, 6, 9, 12]

#tests for multiplying array with array
def test_mul_array(array, other, fail):
    assert array.__mul__(other) == [2, 8, 18, 32]
    assert array.__mul__(fail) == "NotImplemented"

#test for checking if array is identical
def test_eq(array1, array2, array3):
    assert array1.__eq__(array2) == False
    assert array1.__eq__(array3) == False
    assert array1.__eq__(array1) == True

#test for checking which elements are equal to a position in an array
def test_is_equal(array1, array2, element):
    assert array1.is_equal(array2) == [False, False, False, False]
    assert array1.is_equal(element) == [False, False, True, False]

#test for mean of an array
def test_mean(array1, array2):
    assert array1.mean() == 2.5
    assert array2.mean() == 5

#tests for variance of an array
def test_variance(array1, array2):
    assert array1.variance() == 1.25
    assert array2.variance() == 5

#tests for min_element of an array
def test_min_element(array1, array2, array3):
    assert array1.min_element() == 1
    assert array2.min_element() != 5
    assert array3.min_element() == 3


shape = (4,)
shape2 = (5,)
shape2d = (2, 3)
#test2dArray = Array(shape, 3, 3, 5, 9, 11, 1)
testArray = Array(shape, 1, 2, 3, 4)
testArray2 = Array(shape, 2, 4, 6, 8)
failarray = Array(shape2, 4, 4, 5, 3, 9)
otherElement = 5
number = 3
otherArray = [5, 6, 7, 8]
#print(testArray)
test_print(testArray, testArray2)
test_add_element(testArray, otherElement, number)
test_add_array(testArray, testArray2, failarray)
test_sub_element(testArray, otherElement, number)
test_sub_array(testArray, testArray2, failarray)
test_mul_element(testArray, otherElement, number)
test_mul_array(testArray, testArray2, failarray)
test_eq(testArray, testArray2, failarray)
test_is_equal(testArray, testArray2, number)
test_mean(testArray, testArray2)
test_variance(testArray, testArray2)
test_min_element(testArray, testArray2, failarray)
