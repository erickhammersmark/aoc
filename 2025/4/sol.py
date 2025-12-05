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
board = Board(lines, filename=args.filename, example=args.example)

def v(rc):
    return board[rc[board.R]][rc[board.C]] 

count = 0

def wtf(board, pos, neighbors):
    for row, line in enumerate(board):
        for col, cell in enumerate(line):
            rc = (row, col)
            if rc == pos:
                print("X", end="")
            elif rc in neighbors:
                print("N", end="")
            else:
                print(v(rc), end="")
       	print(f"    {''.join(line)}")

if not args.two:
    for row, line in enumerate(board):
        for col, cell in enumerate(line):
            rc = (row, col)
            if v(rc) != "@":
                continue
            atneighs = list(
                        filter(
                            lambda rc: v(rc) == "@",
                            board.neighbors(rc, diagonal=True)
                        )
                    )
            if len(atneighs) < 4:
                count += 1

    print(count)
    sys.exit()

# two

count = 0
while True:
    iter_count = 0
    for row, line in enumerate(board):
        for col, cell in enumerate(line):
            rc = (row, col)
            if v(rc) != "@":
                continue
            atneighs = list(
                        filter(
                            lambda rc: v(rc) == "@",
                            board.neighbors(rc, diagonal=True)
                        )
                    )
            if len(atneighs) < 4:
                board[row][col] = "x"
                iter_count += 1
    count += iter_count
    if iter_count == 0:
        break
print(count)
