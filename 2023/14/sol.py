#!/usr/bin/env python

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

def transpose(board):
    result = []
    for idx in range(len(board[0]) - 1, -1, -1):
       result.append(''.join(line[idx] for line in board))
    return result

lines = read_input(filename=args.filename)
board = transpose(lines)

total = 0
for line in board:
    mag = len(lines)
    for idx, spot in enumerate(line):
        if spot == "O":
            total += mag
            mag -= 1
        elif spot == "#":
            mag = len(lines) - idx - 1
print(total)
