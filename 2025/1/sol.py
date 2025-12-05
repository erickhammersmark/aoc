#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    parser.add_argument("--example", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

lines = read_input(filename="example.txt" if args.example else args.filename)
#board = Board(lines, filename=args.filename, example=args.example)

pos = 50
count = 0

for line in lines:
    sign = 1  # R
    if line[0] == "L":
        sign = -1
    dist = int(line[1:]) * sign
    pos += dist
    pos = pos % 100
    if pos == 0:
        count += 1
print(count)

pos = 50
count = 0

for line in lines:
    sign = 1  # R
    if line[0] == "L":
        sign = -1

    dist = int(line[1:])

    while dist:
        pos += sign
        dist -= 1

        if pos == 100:
            pos = 0
        elif pos == -1:
            pos = 99

        if pos == 0:
            count += 1

print(count)


