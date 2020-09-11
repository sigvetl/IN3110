#!/usr/bin/env python3

class Array:
    # Assignment 3.3

    def __init__(self, shape, *values):
        """
        Initializing array differently depending on the length of the shape tuple.
        This version only works for one- and two-dimensional arrays.
        Checks type of first value in input and returns ValueError if any of the other values not are the same.
        Checking that the number of values are the same as lenght of the shape tuple.
        Depending on 1 or 2-dimensional, initializes through appending via one or two for-loops
        """
        self.array = []
        number = (int, float)
        self.shape = shape
        if isinstance(values[0], number):
            type = number
        elif isinstance(values[0], bool):
            type = bool
        if len(shape) == 2:
            counter = 0
            if (self.shape[0] * self.shape[1]) != len(values):
                raise ValueError("Shape is not equal to number of values")
            for i in range(self.shape[0]):
                new = []
                for j in range(self.shape[1]):
                    if not isinstance(values[counter], type):
                        raise ValueError("Values are not of same type")
                    else:
                        new.append(values[counter])
                        counter+=1
                self.array.append(new)
        elif len(shape) == 1:
            if self.shape[0] != len(values):
                raise ValueError("Shape is not equal to number of values")
            for i in values:
                if not isinstance(i, type):
                    raise ValueError("Values are not of same type")
                else:
                    self.array.append(i)


    def __str__(self):
        stringrep = "["
        if len(self.shape) == 2:
            for i in range(len(self.array)):
                stringrep += "["
                for j in range(self.shape[1]):
                    stringrep += str(self.array[i][j])
                    if (j != self.shape[1] -1):
                        stringrep += ", "
                stringrep += "]"
        else:
            for i in range(len(self.array)):
                stringrep+= str(self.array[i])
                if (i != len(self.array)-1):
                    stringrep+= ", "
        stringrep+= "]"
        return stringrep

        """
        Initializing and ending string with []. For two-dimensional: concatenating new list for
        length of first loop and the values separated by ", " in the second loop.
        For one-dimensional: concatenating the values separated by ", " in the first loop.
        """

    def __add__(self, other):
        """
        Takes an array and an argument (array or number)
        Depending on input is array or number, extracting the values from the one-
        or two-dimensional array and adding it to the other element. In the other array, the value is
        accessed at the same time as the value in the original array. Because of this, a maximum of two
        loops are needed to build the flattened list that the new list take as input.
        """
        newArray = []
        if isinstance(other, (int, float)):
            for i in range(len(self.array)):
                if len(self.shape) == 2:
                    for j in range(self.shape[1]):
                        newArray.append(self.array[i][j] + other)
                else:
                    newArray.append(self.array[i] + other)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    if len(self.shape) == 2:
                        for j in range(self.shape[1]):
                            newArray.append(self.array[i][j] + other.array[i][j])
                    else:
                        newArray.append(self.array[i] + other.array[i])
            else:
                return NotImplemented
        else:
            return NotImplemented
        returnArray = Array(self.shape, *newArray)
        return returnArray

    def __radd__(self, other):
        """
        Same function as above. Being called with flipped arguments.
        """
        newArray = []
        if isinstance(other, (int, float)):
            for i in range(len(self.array)):
                if len(self.shape) == 2:
                    for j in range(self.shape[1]):
                        newArray.append(self.array[i][j] + other)
                else:
                    newArray.append(self.array[i] + other)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    if len(self.shape) == 2:
                        for j in range(self.shape[1]):
                            newArray.append(self.array[i][j] + other.array[i][j])
                    else:
                        newArray.append(self.array[i] + other.array[i])
            else:
                return NotImplemented
        else:
            return NotImplemented
        returnArray = Array(self.shape, *newArray)
        return returnArray

    def __sub__(self, other):
        """
        Takes an array and an argument (array or number)
        Depending on input is array or number, extracting the values from the one-
        or two-dimensional array and subtracting the other element. In the other array, the value is
        accessed at the same time as the value in the original array. Because of this, a maximum of two
        loops are needed to build the flattened list that the new list take as input.
        """
        newArray = []
        if isinstance(other, (int, float)):
            for i in range(len(self.array)):
                if len(self.shape) == 2:
                    for j in range(self.shape[1]):
                        newArray.append(self.array[i][j] - other)
                else:
                    newArray.append(self.array[i] - other)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    if len(self.shape) == 2:
                        for j in range(self.shape[1]):
                            newArray.append(self.array[i][j] - other.array[i][j])
                    else:
                        newArray.append(self.array[i] - other.array[i])
            else:
                return NotImplemented
        else:
            return NotImplemented
        returnArray = Array(self.shape, *newArray)
        return returnArray

    def __rsub__(self, other):
        """
        Same function as above. Being called with flipped arguments.
        """
        newArray = []
        if isinstance(other, (int, float)):
            for i in range(len(self.array)):
                if len(self.shape) == 2:
                    for j in range(self.shape[1]):
                        newArray.append(self.array[i][j] - other)
                else:
                    newArray.append(self.array[i] - other)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    if len(self.shape) == 2:
                        for j in range(self.shape[1]):
                            newArray.append(self.array[i][j] - other.array[i][j])
                    else:
                        newArray.append(self.array[i] - other.array[i])
            else:
                return NotImplemented
        else:
            return NotImplemented
        returnArray = Array(self.shape, *newArray)
        return returnArray


    def __mul__(self, other):
        """
        Takes an array and an argument (array or number)
        Depending on input is array or number, extracting the values from the one-
        or two-dimensional array and multiplying it with the other element. In the other array, the value is
        accessed at the same time as the value in the original array. Because of this, a maximum of two
        loops are needed to build the flattened list that the new list take as input.
        """
        newArray = []
        if isinstance(other, (int, float)):
            for i in range(len(self.array)):
                if len(self.shape) == 2:
                    for j in range(self.shape[1]):
                        newArray.append(self.array[i][j] * other)
                else:
                    newArray.append(self.array[i] * other)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    if len(self.shape) == 2:
                        for j in range(self.shape[1]):
                            newArray.append(self.array[i][j] * other.array[i][j])
                    else:
                        newArray.append(self.array[i] * other.array[i])
            else:
                return NotImplemented
        else:
            return NotImplemented
        returnArray = Array(self.shape, *newArray)
        return returnArray
        """Element-wise multiplies this Array with a number or array.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.
        Returns:
            Array: a new array with every element multiplied with `other`.
        """

    def __rmul__(self, other):
        """
        Same function as above. Being called with flipped arguments.
        """
        newArray = []
        if isinstance(other, (int, float)):
            for i in range(len(self.array)):
                if len(self.shape) == 2:
                    for j in range(self.shape[1]):
                        newArray.append(self.array[i][j] * other)
                else:
                    newArray.append(self.array[i] * other)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    if len(self.shape) == 2:
                        for j in range(self.shape[1]):
                            newArray.append(self.array[i][j] * other.array[i][j])
                    else:
                        newArray.append(self.array[i] * other.array[i])
            else:
                return NotImplemented
        else:
            return NotImplemented
        returnArray = Array(self.shape, *newArray)
        return returnArray


    def __eq__(self, other):
        """
        Comparing length of the two arrays taken as input.
        Checking if elements does not match and returns False, else True
        """
        if len(self.array) == len(other.array):
            for i in range(len(self.array)):
                if len(self.shape) == 2:
                    for j in range(self.shape[1]):
                        if self.array[i][j] != other.array[i][j]:
                            return False
                else:
                    if self.array[i] != other.array[i]:
                        return False
            return True
        else:
            return False

    def is_equal(self, other):
        """
        Building a flattened array with boolean values depending on positional value of one array
        equals that of another array or a given value. Iterates through the arrays through one or two for-loops
        appending True or False depending on the match. For arrays with unequal shape, a ValueError is raised.
        Returning a new array with the same shape as the original and the new values of the flattened array.

        """
        newArray = []
        if isinstance(other, (int, float)):
            for i in range(len(self.array)):
                if len(self.shape) == 2:
                    for j in range(self.shape[1]):
                        if self.array[i][j] != other:
                            newArray.append(False)
                        else:
                            newArray.append(True)
                else:
                    if self.array[i] != other:
                        newArray.append(False)
                    else:
                        newArray.append(True)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    if len(self.shape) == 2:
                        for j in range(self.shape[1]):
                            if self.array[i][j] != other.array[i][j]:
                                newArray.append(False)
                            else:
                                newArray.append(True)
                    else:
                        if self.array[i] != other.array[i]:
                            newArray.append(False)
                        else:
                            newArray.append(True)
            else:
                raise ValueError("Shapes are not equal")
        returnArray = Array(self.shape, *newArray)
        return returnArray

    def mean(self):
        """
        adds every value to the total and returns the total divided by the number of values.
        """
        total = 0
        lengde = 1
        for i in self.shape:
            lengde *= i
        for i in range(len(self.array)):
            if len(self.shape) == 2:
                for j in range(self.shape[1]):
                    total += self.array[i][j]
            else:
                total += self.array[i]
        return total/lengde

    def variance(self):
        """
        adds the variance of every value and returns the total variance divided by the number of values
        """
        lengde = 1
        for i in self.shape:
            lengde *= i
        variance = 0
        mean = self.mean()
        for i in range(len(self.array)):
            if len(self.shape) == 2:
                for j in range(self.shape[1]):
                    variance += ((self.array[i][j] - mean)**2)
            else:
                variance += ((self.array[i] - mean)**2)
        return variance/lengde

    def min_element(self):
        """
        sets the minimum value to the first element of the array. Iterates through
        the rest of the values and sets the minimum to the next value if it is smaller than
        the current minimum.
        """
        if len(self.shape) == 2:
            min = self.array[0][0]
            for i in range(len(self.array)):
                for j in range(self.shape[1]):
                    if self.array[i][j] < min:
                        min = self.array[i][j]
        else:
            min = self.array[0]
            for i in self.array:
                if i < min:
                    min = i
        return min
