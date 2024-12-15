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

board = Board(filename=args.filename, try_type=int)

def walk_trails(pos):
    """
    Walk the tail from a position, advancing only
    to orthogonally adjacent positions with a value
    one greater than the current value. Return the
    positions of all of the nines reached as a
    list (dupes included).
    """
    val = board.get(pos)
    if val == 9:
        return [pos]
    nines = []
    for child in board.neighbors(pos, diagonal=False):
        if board.get(child) == ".":
            continue
        if board.get(child) - val == 1:
            nines.extend(walk_trails(child))
    return nines

count = 0
for idx, row in enumerate(board):
    for col, val in enumerate(row):
        if val == 0:
            nines = walk_trails((idx, col))
            if not args.two:
                nines = set(nines)
            count += len(nines)
print(count)
