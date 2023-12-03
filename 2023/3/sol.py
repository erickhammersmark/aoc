#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import read_input

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    return parser.parse_args()

directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

def check_for_part(grid, y_idx, x_idx):
    for direction in directions:
        y = y_idx + direction[0]
        x = x_idx + direction[1]
        if y < 0 or x < 0 or y >= len(grid) or x >= len(grid[y]):
            continue
        if grid[y][x].isdigit() or grid[y][x] == ".":
            continue
        return True
    return False

def main():
    args = parse_args()
    grid = []
    for line in read_input(filename=args.filename):
        grid.append(line)
    numbers = []
    number = ""
    for y_idx, row in enumerate(grid):
        valid = False
        for x_idx, val in enumerate(row):
            if val.isdigit():
                number = number + val
                if check_for_part(grid, y_idx, x_idx):
                    valid = True
            else:
                if number and valid:
                    numbers.append(int(number))
                number = ""
                valid = False
        if number and valid:
            numbers.append(int(number))
            number = ""
    print(sum(numbers))
        
if __name__ == "__main__":
    main()
