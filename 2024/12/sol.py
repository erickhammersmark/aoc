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

board = Board(filename=args.filename)

AREA = 0
PERIM = 1

def measure_region(pos, visited):
    visited.add(pos)
    plant = board.get(pos)
    price = [1, 0]
    region = set([pos])
    for neigh in board.neighbors(pos, include_oob=True):
        if board.get(neigh) == plant:
            if neigh not in visited:
                region_price, region_cells = measure_region(neigh, visited)
                price = [p + n for p, n in zip(price, region_price)]
                region.update(region_cells)
        else:
            price[PERIM] += 1
    return price, region

def get_outside_dirs(cell):
    dirs = set()
    for neigh in board.neighbors(cell, include_oob=True):
        if board.get(neigh) != board.get(cell):
            dirs.add(board.direction(cell, neigh, english=True))
    return dirs

def skey(pos, _dir):
    return tuple([*pos, _dir])

def find_sides(region):
    """
    Identify all of the "sides" in a region.
    """
    cells = list(region["cells"])
    sides = dict()
    for cell in cells:
        for cell_dir in get_outside_dirs(cell):
            found_side = False
            for side_key, side in sides.items():
                if side["dir"] == cell_dir:
                    points = board.points_between(cell, side["anchor"])
                    if points:
                        if all(board.get(point) == board.get(cell) and cell_dir in get_outside_dirs(point) for point in points):
                            found_side = True
                            side["cells"].add(cell)
                            break # no need to search more sides, but search the rest of the cell's directions
            if not found_side:
                if not all(board.get(neigh) == board.get(cell) for neigh in board.neighbors(cell, include_oob=True)):
                    sides[skey(cell, cell_dir)] = {"anchor": cell, "cells": set([cell]), "dir": cell_dir}
    return sides
        
visited = set()
price = 0
regions = []
for idx, row in enumerate(board):
    for col, plant in enumerate(row):
        if (idx, col) in visited:
            continue
        region_price, region = measure_region((idx, col), visited)
        regions.append({"plant": board.get(list(region)[0]), "cells": region, "area": region_price[AREA], "perim": region_price[PERIM]})
        price += region_price[AREA] * region_price[PERIM]

if args.two:
    price = 0
    for region in regions:
        sides = find_sides(region)
        price += len(sides) * region["area"]

print(price)
