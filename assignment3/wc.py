#!/usr/bin/env python3
import sys

"""Initializes the three variables to 0, opens the file and parsing each line and incrementing
lines, words and chars with a split of " " for words and lenght of line for chars
Skips sys.argv[0] as this is the name of the executable
"""
def wc(fn):
    lines = 0
    words = 0
    chars = 0
    fo = open(fn, "r+")
    for line in fo:
        lines+=1
        words+= len(line.split())
        chars+= len(line)
    print(lines, end = " ")
    print(words, end = " ")
    print(chars, end = " ")
    print(fn)

for number in range(1, len(sys.argv)):
    wc(sys.argv[number])
