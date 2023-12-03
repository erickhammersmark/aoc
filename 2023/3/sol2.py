#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from functools import reduce
from lib import read_input

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    return parser.parse_args()

directions = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

def parse(line):
    """
                                   01234567890123456789
    Parses a line that looks like "..27*..115......@@69." into structs like:
    parts: [("*", (4,)), ("*", (16,)), ("*", (17,))]
    numbers: [("27", (2, 3)), ("115", (7, 8, 9)), ("69", (18, 19))]
    """
    parts = []
    numbers = []
    number = ""
    positions = []
    for idx, char  in enumerate(line):
        if char.isdigit():
            number = number + char
            positions.append(idx)
        else:
            if number:
                numbers.append((number, tuple(positions)))
                number = ""
                positions = []
            if char == ".":
                continue
            parts.append((char, (idx,)))
    if number:
        numbers.append((number, tuple(positions)))
    return parts, numbers
                
def adjacent_numbers(part, numbers):
    """
    Pass this a single part tuple and the three lines surrounding the part.
    """
    target = part[1][0]
    adjacencies = []
    for numberline in numbers:
        for number in numberline:
            if any(abs(n_pos - target) <= 1 for n_pos in number[1]):
                adjacencies.append(number)
    return tuple(adjacencies)

def main():
    args = parse_args()

    parts = []
    numbers = []
    for line in read_input(filename=args.filename):
        line_parts, line_numbers = parse(line)
        parts.append(line_parts)
        numbers.append(line_numbers)

    gear_ratio_sum = 0
    for part_lineno, partline in enumerate(parts):
        for part in partline:
            if part[0] == "*":
                adjacencies = adjacent_numbers(part, numbers[part_lineno-1:part_lineno+2])
                if len(adjacencies) == 2:
                    gear_ratio_sum += reduce(lambda x, y: x * y, [int(adj[0]) for adj in adjacencies])
    print(gear_ratio_sum)


if __name__ == "__main__":
    main()
