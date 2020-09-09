#!/usr/bin/env python3

class Array:
    # Assignment 3.3

    def __init__(self, shape, *values):
        self.array = []
        self.shape = shape[0]
        number = (int, float)
        if isinstance(values[0], number):
            type = number
        elif isinstance(values[0], bool):
            type = bool
        if self.shape != len(values):
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
            for i in self.array:
                newArray.append(i + other)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    newArray.append(self.array[i] + other.array[i])
            else:
                return "NotImplemented"
        else:
            return "NotImplemented"

        return newArray
        """Element-wise adds Array with another Array or number.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to add element-wise to this array.
        Returns:
            Array: the sum as a new array.
        """

    def __radd__(self, other):
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
            for i in self.array:
                newArray.append(i - other)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    newArray.append(self.array[i] - other.array[i])
            else:
                return "NotImplemented"
        else:
            return "NotImplemented"
        return newArray
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
            for i in self.array:
                newArray.append(i * other)
        elif isinstance(other, Array):
            if self.shape == other.shape:
                for i in range(len(self.array)):
                    newArray.append(self.array[i] * other.array[i])
            else:
                return "NotImplemented"
        else:
            return "NotImplemented"


        return newArray
        """Element-wise multiplies this Array with a number or array.
        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.
        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.
        Returns:
            Array: a new array with every element multiplied with `other`.
        """

    def __rmul__(self, other):
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

    def is_equal(self, other):
        newArray = []
        if isinstance(other, (int, float)):
            for i in self.array:
                if i != other:
                    newArray.append(False)
                else:
                    newArray.append(True)
            return newArray
        elif isinstance(other, Array):
            if len(self.array) == len(other.array):
                for i in range(len(self.array)):
                    if self.array[i] != other.array[i]:
                        newArray.append(False)
                    else:
                        newArray.append(True)
                return newArray
            else:
                return False
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
        for i in self.array:
            total += i
        return total/len(self.array)
        """Computes the mean of the array
        Only needs to work for numeric data types.
        Returns:
            float: The mean of the array values.
        """

    def variance(self):
        variance = 0
        mean = self.mean()
        for i in self.array:
            variance += ((i - mean)**2)
        return variance/len(self.array)
        """Computes the variance of the array
        Only needs to work for numeric data types.
        The variance is computed as: mean((x - x.mean())**2)
        Returns:
            float: The mean of the array values.
        """
        pass

    def min_element(self):
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
        pass
