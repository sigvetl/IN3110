#!/usr/bin/env python3

from Array import Array
import pytest

shape = (4,)
shape2 = (5,)
shape2d = (2, 3)
testArray = Array(shape, 1, 2, 3, 4)
testArray2 = Array(shape, 2, 4, 6, 8)
failarray = Array(shape2, 4, 4, 5, 3, 9)
test2d = Array(shape2d, 3, 5, 1, 5, 6, 6)
test2d2 = Array(shape2d, 3, 5, -10, 5, 0, 5)

#print-test
def test_print():
    assert testArray.__str__() == "[1, 2, 3, 4]"
    assert testArray2.__str__() == "[2, 4, 6, 8]"

def test_print_2d():
    assert test2d.__str__() == "[[3, 5, 1][5, 6, 6]]"
    assert test2d2.__str__() == "[[3, 5, -10][5, 0, 5]]"

#tests for adding element to array
def test_add_element():
    assert testArray.__add__(5) == Array((4,), 6, 7, 8, 9)
    assert testArray.__add__(3) == Array((4,), 4, 5, 6, 7)
    assert 5+testArray == Array((4,), 6, 7, 8, 9)
    assert testArray+5 == Array((4,), 6, 7, 8, 9)

#tests for adding array to array
def test_add_array():
    assert testArray.__add__(testArray2) == Array((4,), 3, 6, 9, 12)
    assert testArray.__add__(failarray) == NotImplemented

def test_add_2d():
    assert test2d + test2d2 == Array((2, 3), 6, 10, -9, 10, 6, 11)
    assert test2d + 5 == Array((2, 3), 8, 10, 6, 10, 11, 11)

#tests for subtracting element from array
def test_sub_element():
    assert testArray.__sub__(5) == Array((4,), -4, -3, -2, -1)
    assert testArray.__sub__(3) == Array((4,), -2, -1, 0, 1)

#tests for subtracting array from array
def test_sub_array():
    assert testArray.__sub__(testArray2) == Array((4,), -1, -2, -3, -4)
    assert testArray.__sub__(failarray) == NotImplemented

def test_sub_2d():
    assert test2d - test2d2 == Array((2, 3), 0, 0, 11, 0, 6, 1)
    assert test2d - 5 == Array((2, 3), -2, 0, -4, 0, 1, 1)

#tests for multiplying element with array
def test_mul_element():
    assert testArray.__mul__(5) == Array((4,), 5, 10, 15, 20)
    assert testArray.__mul__(3) == Array((4,), 3, 6, 9, 12)

#tests for multiplying array with array
def test_mul_array():
    assert testArray.__mul__(testArray2) == Array((4,), 2, 8, 18, 32)
    assert testArray.__mul__(failarray) == NotImplemented

def test_mul_2d():
    assert test2d * test2d2 == Array((2, 3), 9, 25, -10, 25, 0, 30)
    assert test2d * 5 == Array((2, 3), 15, 25, 5, 25, 30, 30)

#test for checking if array is identical
def test_eq():
    assert testArray.__eq__(testArray2) == False
    assert testArray.__eq__(failarray) == False
    assert testArray.__eq__(testArray) == True

def test_eq_2d():
    assert test2d != test2d2
    assert test2d == test2d

#test for checking which elements are equal to a position in an array
def test_is_equal():
    assert testArray.is_equal(testArray2) == Array((4,), False, False, False, False)
    assert testArray.is_equal(3) == Array((4,), False, False, True, False)

def test_is_equal_2d():
    assert test2d.is_equal(test2d2) == Array((2, 3), True, True, False, True, False, False)
    assert test2d.is_equal(test2d) == Array((2, 3), True, True, True, True, True, True)

#test for mean of an array
def test_mean():
    assert testArray.mean() == 2.5
    assert testArray2.mean() == 5

def test_mean_2d():
    assert test2d.mean() == pytest.approx(4.333333)
    assert test2d2.mean() == pytest.approx(1.333333)

#tests for variance of an array
def test_variance():
    assert testArray.variance() == 1.25
    assert testArray2.variance() == 5

def test_variance_2d():
    assert test2d.variance() == pytest.approx(3.222222)
    assert test2d2.variance() == pytest.approx(28.888889)

#tests for min_element of an array
def test_min_element():
    assert testArray.min_element() == 1
    assert testArray2.min_element() != 5
    assert failarray.min_element() == 3

def test_min_element_2d():
    assert test2d.min_element() == 1
    assert test2d2.min_element() == -10
