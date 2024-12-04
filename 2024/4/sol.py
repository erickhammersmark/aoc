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

board = [list(line) for line in read_input(filename=args.filename)]
cols = len(board[0])
rows = len(board)
pos = (0, 0) # row, col

def dir_delta(pos_new, pos_old):
    return [pos_new[0] - pos_old[0], pos_new[1] - pos_old[1]]

def neighbors(pos, direction=None):
    neighs = set()
    neigh_rows = [pos[0]]
    neigh_cols = [pos[1]]
    if pos[0] > 0:
        neigh_rows.append(pos[0] - 1)
    if pos[0] < rows - 1:
        neigh_rows.append(pos[0] + 1)
    if pos[1] > 0:
        neigh_cols.append(pos[1] - 1)
    if pos[1] < cols - 1:
        neigh_cols.append(pos[1] + 1)
    for r in neigh_rows:
        for c in neigh_cols:
            if [r,c] == pos:
                continue
            if direction and (r - pos[0] != direction[0] or c - pos[1] != direction[1]):
                continue
            neighs.add((r,c))
    return neighs

def find_xmas(results, remaining_letters, pos, direction=None):
    if not remaining_letters:
        results.append(1)
        return
    
    for neigh in neighbors(pos, direction=direction):
        if board[neigh[0]][neigh[1]] == remaining_letters[0]:
            _dir = direction if direction else dir_delta(neigh, pos)
            find_xmas(results, remaining_letters[1:], neigh, direction=_dir)
    return results

sam_deltas = [[-1, -1], [-1, 1], [1, 1], [1, -1]]
sam_success_cases = ["SSMM", "MSSM", "MMSS", "SMMS"]

def two_sams(a_pos):
    r = a_pos[0]
    c = a_pos[1]
    b = board
    if b[r][c] != "A":
        return False
    if r == 0:
        return False
    if r == rows - 1:
        return False
    if c == 0:
        return False
    if c == cols - 1:
        return False

    xvals = "".join(b[r+d[0]][c+d[1]] for d in sam_deltas)
    if xvals in sam_success_cases:
        return True
    return False


results = []
for r in range(0, rows):
    for c in range(0, cols):
        if args.two:
            if two_sams([r,c]):
                results.append([r,c])
        else:
            if board[r][c] == "X":
                find_xmas(results, "MAS", [r,c], direction=None)
print(len(results))
