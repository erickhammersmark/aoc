#!/usr/bin/env python

import resource
import sys
sys.path.append("..")

from argparse import ArgumentParser
from functools import cache
from lib import *

# here there be dragons
resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
sys.setrecursionlimit(10**6)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    parser.add_argument("--viz", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

north = (0, -1)
south = (0, 1)
east = (1, 0)
west = (-1, 0)

cardinal_cw = (north, east, south, west, north)
cardinal_ccw = (north, west, south, east, north)

dirs = {
    ".": lambda cur, prev: keeponkeepinon(cur, prev),
    "/": lambda cur, prev: ccw(cur, prev) if delta(cur, prev) in (east, west) else cw(cur, prev),
    "\\": lambda cur, prev: cw(cur, prev) if delta(cur, prev) in (east, west) else ccw(cur, prev),
    "|": lambda cur, prev: split(cur, prev) if delta(cur, prev) in (east, west) else keeponkeepinon(cur, prev),
    "-": lambda cur, prev: split(cur, prev) if delta(cur, prev) in (north, south) else keeponkeepinon(cur, prev),
}

@cache
def next_card(cardlist, card):
    return cardlist[cardlist.index(card)+1]

@cache
def delta(cur, prev):
    return (cur[0] - prev[0], cur[1] - prev[1])

@cache
def move(cur, delta):
    return (cur[0] + delta[0], cur[1] + delta[1])

def cw(cur, prev):
    return (move(cur, next_card(cardinal_cw, delta(cur, prev))),)

def ccw(cur, prev):
    return (move(cur, next_card(cardinal_ccw, delta(cur, prev))),)

@cache
def split(cur, prev):
    return cw(cur, prev) + ccw(cur, prev)

@cache
def keeponkeepinon(cur, prev):
    return (move(cur, delta(cur, prev)),)

def get_tile(cur):
    return tiles[cur[1]][cur[0]]

def oob(cur):
    if cur[0] < 0 or cur[0] >= x_oob:
        return True
    if cur[1] < 0 or cur[1] >= y_oob:
        return True
    return False

def solve(cur, prev, visited):
    #print(f"solve({cur}, {prev}, {visited})")
    if args.viz:
        viz(cur, visited)
        input()
    visited.add((cur, prev))
    for potent in dirs[get_tile(cur)](cur, prev):
        #print(f"tile: {get_tile(cur)}, cur: {cur}, prev: {prev}, potent: {potent}, visited: {visited}")
        if oob(potent):
            continue
        if (potent, cur) in visited:
            continue
        solve(potent, cur, visited)

def viz(cur, visited):
    for ridx, row in enumerate(tiles):
        for cidx, tile in enumerate(row):
            if (cidx, ridx) == cur:
                print("C", end="")
            elif any((cidx, ridx) == v[0] for v in visited):
                print("#", end="")
            else:
                print(tile, end="")
        print()

lines = read_input(filename=args.filename)

x_oob = len(lines[0])
y_oob = len(lines)

tiles = [list(line) for line in lines]

if args.two:
    max_len = 0
    for x in range(x_oob):
        # coming in along the top
        visited = set()
        solve((x, 0), (x, -1), visited)
        max_len = max(len(set(v[0] for v in visited)), max_len)
        # and up from the bottom
        visited = set()
        solve((x, y_oob-1), (x, y_oob), visited)
        max_len = max(len(set(v[0] for v in visited)), max_len)
    for y in range(y_oob):
        # from the left
        visited = set()
        solve((0, y), (-1, y), visited)
        max_len = max(len(set(v[0] for v in visited)), max_len)
        # from the right
        visited = set()
        solve((x_oob-1, y), (x_oob, y), visited)
        max_len = max(len(set(v[0] for v in visited)), max_len)
    print(max_len)
else:
    visited = set()
    solve((0,0), (-1, 0), visited)   
    print(len(set(v[0] for v in visited)))

r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
