#!/usr/bin/env python3

"""
On each line, the calibration value can be found by combining the first digit
and the last digit (in that order) to form a single two-digit number.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""

sum = 0
with open("input.txt", "r") as INPUT:
    for line in INPUT.readlines():
        digits = list(filter(lambda x: x >= "0" and x <= "9", line))
        sum += int(digits[0] + digits[-1])
print(sum)

