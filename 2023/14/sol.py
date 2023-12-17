#!/usr/bin/env python

import sys
import time

from argparse import ArgumentParser
from copy import deepcopy

sys.path.append("..")
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

def cw(board):
    """
    NOT in-place, returns brand new board
    """
    return list(list(l) for l in zip(*reversed(board)))

def ccw(board):
    return cw(cw(cw(board)))

lines = [list(line) for line in read_input(filename=args.filename)]

# "up" for us is left, board arrives in west "up" orientation, so we spin it to start at north
board = ccw(lines)

def fall(board):
    """
    Board always falls left.
    Rotate it the way you want before passing it here.
    Modifies board in place
    """
    for line in board:
        places = []
        for idx, val in enumerate(line):
            if val == ".":
                places.append(idx)
            elif val == "O" and places:
                line[places.pop(0)] = "O"
                line[idx] = "."
                places.append(idx)
            elif val == "#":
                places = []

def cycle():
    global board
    """
    Always assuming the board is north "up" (left) when it is passed here.
    """
    fall(board)         # north
    board = cw(board)
    fall(board)         # west
    board = cw(board)
    fall(board)         # south
    board = cw(board)
    fall(board)         # east
    board = cw(board)

def measure():
    total = 0
    for line in board:
        mag = len(line)
        for idx, spot in enumerate(line):
            if spot == "O":
                total += mag - idx
    return total

def print_board(board):
    for line in board:
        print(line)
    print()

# Part 1
fall(board)
print(f"Part 1: {measure()}")

if args.two:
    #boards = []
    scores = []
    for n in range(250):
        cycle()
        scores.append(measure())
        #print(f"Cycle {n}, score: {scores[-1]}")
    loop = None
    for idx, scr in enumerate(scores):
        for pos in range(1, len(scores[idx:])):
            try:
                if scr == scores[idx+pos]:
                    if scr == scores[idx+(pos * 2)]:
                        if scores[idx:idx+pos] == scores[idx+pos:idx+pos*2]:
                            #if loop is None or pos > loop[1] - loop[0]:
                                loop = (idx, idx+pos)
                                break
            except IndexError:
                break
    loop_len = loop[1] - loop[0]
    start = loop[0]
    middle = int((1000000000 - start) / loop_len) * loop_len
    end = 1000000000 - (middle + start)
    print(scores[loop[0] + end - 1])
