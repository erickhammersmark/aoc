#!/usr/bin/env python3

import math

lines = None

with open("input.txt", "r") as INPUT:
    lines = INPUT.readlines()

left = []
right = []
for (l, r) in (line.split() for line in lines):
    left.append(int(l))
    right.append(int(r))

left.sort()
right.sort()

# part 1
distance = 0
for l, r in zip(left, right):
    distance += abs(l - r)
print(distance)

# part 2
similarity = 0
r_pos = 0
for l in left:
    while r_pos < len(right) and right[r_pos] < l:
        r_pos += 1
    while r_pos < len(right) and right[r_pos] == l:
        similarity += l
        r_pos += 1
print(similarity)
