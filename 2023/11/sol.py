#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from itertools import combinations
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

orig_lines = read_input(filename=args.filename)

# append the lines without galaxies twice
lines = []
rows_to_double = []
for idx, line in enumerate(orig_lines):
    if "#" not in line:
        rows_to_double.append(idx)
        lines.append(line)
    lines.append(line)

# find the columns with no galaxies
counts = [0] * len(lines[0])
for idx, line in enumerate(lines):
    try:
        idx = -1
        while True:
            idx = line.index("#", idx+1)
            counts[idx] += 1
    except ValueError:
        pass

# double the columns with no galaxies
cols_to_double = list(idx for idx, count in enumerate(counts) if count == 0)
for idx, line in enumerate(lines):
    for modifier, col in enumerate(cols_to_double):
        line = line[:col+modifier] + "." + line[col+modifier:]
    lines[idx] = line

# find all of the galaxies
galaxies = []
for y, line in enumerate(lines):
    try:
        idx = -1
        while True:
            idx = line.index("#", idx+1)
            galaxies.append((idx, y))
    except ValueError:
        pass

# generate all the combinations of galaxies
pairs = list(combinations(galaxies, 2))

# up/down/left/right distances are always the same, as long as you proceed toward the destination
print(f"Part 1: {sum(abs(dest[0] - src[0]) + abs(dest[1] - src[1]) for src, dest in pairs)}")

if not args.two:
    sys.exit(0)

# PART TWO LET'S GOOOO

# find all of the galaxies again
galaxies = []
for y, line in enumerate(orig_lines):
    try:
        idx = -1
        while True:
            idx = line.index("#", idx+1)
            galaxies.append((idx, y))
    except ValueError:
        pass

# generate all the combinations again
pairs = list(combinations(galaxies, 2))

# calculate the distances WAAAAY different
_sum = 0
for pair in pairs:
    horiz = [galaxy[0] for galaxy in pair]
    vert = [galaxy[1] for galaxy in pair]
    left = min(horiz)
    right = max(horiz)
    top = min(vert)
    bottom = max(vert)

    delta_x = right - left
    delta_y = bottom - top

    for col in cols_to_double:
        if left < col < right:
            delta_x += 999999
    for row in rows_to_double:
        if top < row < bottom:
            delta_y += 999999

    _sum += delta_x + delta_y

print(_sum)
