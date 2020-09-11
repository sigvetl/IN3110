#!/usr/bin/env python3

class Array:
    # Assignment 3.3

    def __init__(self, shape, *values):
        self.array = []
        number = (int, float)
        if len(shape) == 2:
            counter = 0
            #two dimensional
            self.shape = shape
            if isinstance(values[0], number):
                type = number
            elif isinstance(values[0], bool):
                type = bool
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
            self.shape = shape
            if isinstance(values[0], number):
                type = number
            elif isinstance(values[0], bool):
                type = bool
            if self.shape[0] != len(values):
                raise ValueError("Shape is not equal to number of values")
            for i in values:
                if not isinstance(i, type):
                    raise ValueError("Values are not of same type")
                else:
                    self.array.append(i)

        """
        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).
        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either numeric or boolean.
        Raises:
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """

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

        """Returns a nicely printable string representation of the array.
        Returns:
            str: A string representation of the array.
        """

    def __add__(self, other):
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
        """Element-wise adds Array with another Array or number.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to add element-wise to this array.
        Returns:
            Array: the sum as a new array.
        """

    def __radd__(self, other):
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
        """Element-wise adds Array with another Array or number.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to add element-wise to this array.
        Returns:
            Array: the sum as a new array.
        """
        pass

    def __sub__(self, other):
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
        """Element-wise subtracts an Array or number from this Array.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.
        Returns:
            Array: the difference as a new array.
        """
        pass

    def __rsub__(self, other):
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
        """Element-wise subtracts this Array from a number or Array.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number being subtracted from.
        Returns:
            Array: the difference as a new array.
        """
        pass

    def __mul__(self, other):
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
        pass

    def __eq__(self, other):
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
        """Compares an Array with another Array.
        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.
        Args:
            other (Array): The array to compare with this array.
        Returns:
            bool: True if the two arrays are equal. False otherwise.
        """
    #mangler
    def is_equal(self, other):
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
            if len(self.array) == len(other.array):
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
                return False
        returnArray = Array(self.shape, *newArray)
        return returnArray
        """Compares an Array element-wise with another Array or number.
        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        Args:
            other (Array, float, int): The array or number to compare with this array.
        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.
        Raises:
            ValueError: if the shape of self and other are not equal.
        """

    def mean(self):
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
        """Computes the mean of the array
        Only needs to work for numeric data types.
        Returns:
            float: The mean of the array values.
        """

    def variance(self):
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
        """Computes the variance of the array
        Only needs to work for numeric data types.
        The variance is computed as: mean((x - x.mean())**2)
        Returns:
            float: The mean of the array values.
        """

    def min_element(self):
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
        """Returns the smallest value of the array.
        Only needs to work for numeric data types.
        Returns:
            float: The value of the smallest element in the array.
        """
