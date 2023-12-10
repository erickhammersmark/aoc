#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

import resource
resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
sys.setrecursionlimit(10**6)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

north = (0, -1)
south = (0, 1)
east = (1, 0)
west = (-1, 0)

dirs = {
    "|": (north, south),
    "-": (east, west),
    "L": (north, east),
    "J": (north, west),
    "7": (south, west),
    "F": (south, east),
    ".": (),
    "S": (north, south, east, west),
}

class Tile(object):
    def __init__(self, pos, char):
        self.pos = pos
        self.char = char
        self.dirs = dirs[char]

    def __repr__(self):
        return f"{self.char} at {self.pos}"

    def add_pos(self, a, b):
        return tuple(map(lambda x,y: x+y, a, b))

    def is_complementary(self, a, b):
        if not a or not b:
            return False
        if a == (0, 0) or b == (0, 0):
            return False
        if self.add_pos(a, b) == (0, 0):
            return True
        return False

    def links(self, board):
        links = []
        for _dir in self.dirs:
            x, y = self.add_pos(self.pos, _dir)
            neighbor = board[y][x]
            for ndir in neighbor.dirs:
                if self.is_complementary(_dir, ndir):
                    links.append(neighbor)
                    break
        return links

board = []
S = None
for y, line in enumerate(read_input(filename=args.filename)):
    board.append([Tile((idx, y), char) for idx, char in enumerate(line)])
    if "S" in line:
        S = board[y][line.index("S")]

#print(f"S: {S.pos} with links {S.links(board)}")

def find_path(prev, tile, count):
    if count > 1 and tile.char == "S":
        return count

    for link in tile.links(board):
        if link == prev:
            continue

        print(tile)
        new_count = find_path(tile, link, count + 1)
        if new_count:
            return new_count

    return 0

print(find_path(None, S, 0))
"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""






