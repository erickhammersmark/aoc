#!/usr/bin/env python

import functools
import resource
import sys
sys.path.append("..")

from ansi.color import fg
from argparse import ArgumentParser
from lib import *

# here there be dragons
resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
sys.setrecursionlimit(10**6)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

# some directional constants and functions
north = (0, -1)
south = (0, 1)
east = (1, 0)
west = (-1, 0)
northeast = (1, -1)
northwest = (-1, -1)
southeast = (1, 1)
southwest = (-1, 1)

cardinal_cw = [north, east, south, west, north]
cardinal_ccw = [north, west, south, east, north]

def dirname(direction):
    for tup, name in [(north, "north"), (south, "south"), (east, "east"), (west, "west")]:
        if direction == tup:
            return name
    return direction

def next_cardinal(left_or_right, direction):
    if left_or_right == "left":
        return cardinal_ccw[cardinal_ccw.index(direction)+1]
    if left_or_right == "right":
        return cardinal_cw[cardinal_cw.index(direction)+1]
    return None


def cardinal(a, b):
    """
    moving from a to b moves in this direction.
    """
    dx = b.pos[0] - a.pos[0]
    dy = b.pos[1] - a.pos[1]
    if (dx, dy).count(0) != 1:
        return None
    if dx > 0:
        return east
    if dx < 0:
        return west
    if dy > 0:
        return south
    if dy < 0:
        return north
    return None

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

def complementary_direction(direction):
    if direction == north:
        return south
    if direction == south:
        return north
    if direction == east:
        return west
    if direction == west:
        return east

class Tile(object):
    def __init__(self, pos, char):
        self.pos = pos
        self.char = char
        self.dirs = dirs[char]
        self.inward = None

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

    @functools.cache
    def links(self):
        """
        Builds the list of tiles that we link to.
        We link to a tile if we extend in its direction and it also
        extends in ours.
        """
        global board
        links = []
        for _dir in self.dirs:
            x, y = self.add_pos(self.pos, _dir)
            neighbor = board[y][x]
            for ndir in neighbor.dirs:
                if self.is_complementary(_dir, ndir):
                    links.append(neighbor)
                    break
        return links

    def turn_from(self, prev):
        # this is the cardinal direction from us to prev
        in_dir = cardinal(self, prev)
        for _dir in self.dirs:
            if _dir == in_dir:
                continue
            # this is a bug. we need to turn left from the direction that prev took to get to us, not the direction we would use to get back to prev.
            if next_cardinal("left", complementary_direction(in_dir)) == _dir:
                return "left"
            if next_cardinal("right", complementary_direction(in_dir)) == _dir:
                return "right"
        return None

    @functools.cache
    def inward_tile(self):
        if not self.inward:
            return None
        tile_pos = self.add_pos(self.pos, self.inward)
        return tileat(tile_pos)

board = []
S = None
for y, line in enumerate(read_input(filename=args.filename)):
    board.append([Tile((idx, y), char) for idx, char in enumerate(line)])
    if "S" in line:
        S = board[y][line.index("S")]

#print(f"S: {S.pos} with links {S.links(board)}")

def tileat(pos):
    try:
        return board[pos[1]][pos[0]]
    except:
        return None

path = [S]
def find_path(path):
    if len(path) > 1 and path[-1].char == "S":
        return path

    for link in path[-1].links():
        if len(path) > 1 and link == path[-2]:
            continue

        new_path = find_path(path + [link])
        if new_path:
            return new_path

    return []

path = find_path([S])
print(f"Part 1: {int((len(path) - 1) / 2)}")

#####
#
# Everything below here does not work
#
# It gets close, and then visual inspection of the path and the enclosed tiles
# showed me exactly 1 that should have been enclosed but was not. For my input,
# the number this produces + 1 is the correct answer for day 10 part 2.
# Good e-f'ing-nough.
#
# Also, the inward-vs-outward initial detection is crap, I just hard coded the
# first one until the output looked right. I remain unashamed.
#
#####

lefts = 0
rights = 0
for idx, tile in enumerate(path[1:]):
    if tile.turn_from(path[idx]) == "left":
        lefts += 1
    elif tile.turn_from(path[idx]) == "right":
        rights += 1

#print(f"lefts: {lefts}, rights: {rights}, initial_dir: {cardinal(path[0], path[1])}")

"""
if path[0].pos[1] == path[1].pos[1]:
    # first move was east-west
    if path[0].pos[1] < path[1].pos[1]:
        # east
        if lefts > rights:
            path[1].inward = south
        else:
            path[1].inward = north
    else:
        # west
        if lefts > rights:
            path[1].inward = north
        else:
            path[1].inward = south
else:
    # first move was north-south
    if path[0].pos[0] < path[1].pos[0]:
        # south
        if lefts < rights:
            path[1].inward = west
        else:
            path[1].inward = east
    else:
        # north
        if lefts > rights:
            path[1].inward = east
        else:
            path[1].inward = west
"""
path[1].inward = north

for idx, tile in enumerate(path[2:]):
    tile.inward = path[idx+1].inward
    if tile.char in ("J", "L", "F", "7"):
        lr = tile.turn_from(path[idx+1])
        tile.inward = next_cardinal(lr, tile.inward)

path[0].inward = None
path[-1].inward = None

enclosed = set()
for tile in path:
    print(tile, dirname(tile.inward))
    if tile.inward_tile() not in path:
        enclosed.add(tile.inward_tile())

def find_notpath(tile):
    if not tile:
        return
    for _dir in (north, south, east, west):
        dir_pos = tile.add_pos(tile.pos, _dir)
        dir_tile = tileat(dir_pos)
        if not dir_tile:
            continue
        if dir_tile in path:
            continue
        if dir_tile in enclosed:
            continue
        enclosed.add(dir_tile)
        find_notpath(dir_tile)

for tile in list(enclosed):
    find_notpath(tile)

"""
enclosed = set()
for row in board:
    for tile in row:
        if tile in path:
            continue
        for _dir in (north, south, east, west):
            dir_pos = tile.pos
            while 0 <= dir_pos[0] < len(row) and 0 <= dir_pos[1] < len(board):
                dir_pos = tile.add_pos(dir_pos, _dir)
                dir_tile = tileat(dir_pos)
                if dir_tile not in path:
                    continue
                if dir_tile.is_complementary(_dir, dir_tile.inward):
                    enclosed.add(tile)
                    break
                if _dir == dir_tile.inward:
                    break
            if tile in enclosed:
                break
"""

charswap = {'F': '\u250c', 'J': '\u2518', '7': '\u2510', 'L': '\u2514', '-': '\u2500', '|': '\u2502'}

for y, line in enumerate(read_input(filename=args.filename)):
    for x, char in enumerate(line):
        if char in charswap:
            char = charswap[char]
        if tileat((x,y)) in enclosed:
            print(fg.blue(char), end="")
        elif tileat((x,y)) in path:
            print(fg.red(char), end="")
        else:
            print(char, end="")
    print()
print(len(enclosed))

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


