#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

from collections import defaultdict

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

antennas = defaultdict(list)
board = read_input(filename=args.filename)
boardlist = []
for idx, row in enumerate(board):
    boardlist.append(list(row))
    for col, val in enumerate(row):
        if val == ".":
            continue
        antennas[val].append((idx, col))

def inbounds(antinode):
    row, col = antinode
    if row < 0 or col < 0:
        return False
    if row >= len(board) or col >= len(board[0]):
        return False
    return True

def pos_difference(_from, _to):
    dr = _to[0] - _from[0]
    dc = _to[1] - _from[1]
    return (dr, dc)

def add_pos(a, b):
    return (a[0] + b[0], a[1] + b[1])

def sub_pos(a, b):
    return (a[0] - b[0], a[1] - b[1])

def find_antinodes(a, b, two=False):
    delta_p = pos_difference(a, b)
    antinodes = set([a, b])
    a = sub_pos(a, delta_p)
    while inbounds(a):
        antinodes.add(a)
        if not two:
            break
        a = sub_pos(a, delta_p)
    b = add_pos(b, delta_p)
    while inbounds(b):
        antinodes.add(b)
        if not two:
            break
        b = add_pos(b, delta_p)
    return antinodes

antinodes = set()

for antenna, locations in antennas.items():
    for first_location in locations:
        for second_location in locations:
            if first_location == second_location:
                continue
            antinodes = antinodes.union(find_antinodes(first_location, second_location, two=args.two))
for antinode in antinodes:
    boardlist[antinode[0]][antinode[1]] = "#"
for line in boardlist:
    print("".join(line))
print(len(antinodes))
