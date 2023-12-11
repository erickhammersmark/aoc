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

# append the lines without galaxies twice
lines = []
for line in read_input(filename=args.filename):
    if "#" not in line:
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
print(sum(abs(dest[0] - src[0]) + abs(dest[1] - src[1]) for src, dest in pairs))
