#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

from collections import defaultdict
from copy import copy, deepcopy

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

guard_chars = "^>v<"
guard_init_char = ""
guard_init_pos = (-1, -1)

board = read_input(filename=args.filename)
for idx, line in enumerate(board):
    for gc in guard_chars:
        if gc in line:
            guard_init_char = gc
            guard_init_pos = (idx, line.index(gc))

def oob(board, row, col):
    if row < 0 or col < 0:
        return True
    if row > len(board) - 1 or col > len(board[0]) - 1:
        return True
    return False

def walk(board, guard_pos, guard_char, two=True):
    row, col = guard_pos
    next_row = row
    next_col = col
    visited = defaultdict(set)
    loop_count = 0
    while True:
        row, col = guard_pos
        next_row = row
        next_col = col
        if guard_char == "^":
            next_row -= 1
        elif guard_char == "v":
            next_row += 1
        elif guard_char == "<":
            next_col -= 1
        elif guard_char == ">":
            next_col += 1
        else:
            print(f"unknown guard char {guard_char}")
        if oob(board, next_row, next_col):
            if not two:
                print(len(visited) + 1)
            return loop_count
        visited[guard_pos].add(guard_char)
        if board[next_row][next_col] == "#":
            idx = guard_chars.index(guard_char) + 1
            if idx >= len(guard_chars):
                idx = 0
            guard_char = guard_chars[idx]
        else:
            if guard_char in visited.get((next_row, next_col), []):
                return "loop"
                
            guard_pos = (next_row, next_col)


if args.two:
    loop_count = 0
    for _row in range(0, len(board)):
        for _col in range(0, len(board[0])):
            if board[_row][_col] == "#":
                continue
            _board = copy(board)
            line = list(_board[_row])
            line[_col] = "#"
            _board[_row] = "".join(line)
            result = walk(_board, guard_init_pos, guard_init_char)
            if result == "loop":
                loop_count += 1
    print(loop_count)
else:
    walk(board, guard_init_pos, guard_init_char, two=args.two)
