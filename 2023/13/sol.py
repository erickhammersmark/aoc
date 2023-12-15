#!/usr/bin/env python

import math
import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

patterns = [[]]
for line in read_input(filename=args.filename):
    if not line:
        patterns.append([])
        continue
    patterns[-1].append(line)

with open("right_answers.txt", "r") as RIGHT:
    correct = [line.rstrip() for line in RIGHT.readlines()]

def print_pattern(pat):
    for line in pat:
        print(line)

def transpose(pattern):
    result = []
    for idx in range(len(pattern[0]) - 1, -1, -1):
       result.append(''.join(line[idx] for line in pattern))
    return result 

def score(pattern):
    # find all the possible midpoints on each line and their widths
    all_lines_midpoints = []
    for line in pattern:
        midpoints = set()
        for idx in range(len(line)-1):
            if line[idx] == line[idx+1]:
                width = 2
                lx = idx-1
                rx = idx+2
                while lx >= 0 and rx < len(line) and line[lx] == line[rx]:
                    width += 2
                    lx -= 1
                    rx += 1
                if lx == -1 or rx == len(line):
                    midpoints.add((idx + 0.5, width))
        all_lines_midpoints.append(midpoints)

    # mp becomes a set of midpoints that are common among all rows
    mp = set([m[0] for m in all_lines_midpoints[0]])
    for mp_set in all_lines_midpoints:
        mp = mp.intersection(set([m[0] for m in mp_set]))

    # weighted_mps becomes a list of tuples
    # first element is the min width of a reflection around a midpoint across all lines
    # second element is the index to the right of the midpoint
    weighted_mps = [(min([wp[1] for midpoints in all_lines_midpoints for wp in midpoints if wp[0] == m]), int(m)+1) for m in mp]
    if not weighted_mps:
        return (0, 0)
    #if all(wmp[0] <= 2 for wmp in weighted_mps):
    #    return (0, 0)

    # sort on the minimum reflected width around each line of reflection
    weighted_mps.sort()

    # biggest minimum reflection width wins
    return weighted_mps[-1]

total = 0
for idx, pattern in enumerate(patterns):
    left = score(pattern)
    top = score(transpose(pattern))
    if idx == 8:
        print_pattern(pattern)
        print(left)
        print()
        print_pattern(transpose(pattern))
        print(top)
        print()
        print()
        print(f"{idx} Our answer: ", end="")
        if left[0] > top[0]:
            print(left[1], end=", ")
        else:
            print(100 * top[1], end=", ")
        print(f"correct answer: {correct[idx]}") 
    if left[0] > top[0]:
        total += left[1]
    else:
        total += 100 * top[1]
print(total)
