#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

import re

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    parser.add_argument("--example", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

if args.example:
    COLS = 11
    ROWS = 7
else:
    COLS = 101
    ROWS = 103

lines = read_input(filename="example.txt" if args.example else args.filename)
#board = Board(lines, filename=args.filename, example=args.example)

robot_re = re.compile(r"p=(?P<x>[0-9]+),(?P<y>[0-9]+)\sv=(?P<vx>[-]?[0-9]+),(?P<vy>[-]?[0-9]+)")

class Robot(tuple):
    def __init__(self, *args, **kwargs):
        super().__init__()
    
    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def vx(self):
        return self[2]

    @property
    def vy(self):
        return self[3]

def print_robots(robots):
    area = []
    for _ in range(0, ROWS):
        area.append(["."] * COLS)
    for rb in robots:
        if area[rb.y][rb.x] == ".":
            area[rb.y][rb.x] = 1
        else:
            area[rb.y][rb.x] += 1
    for line in area:
        print("".join(map(str,line)))

robots = []
for line in lines:
    robots.append(Robot(tuple(map(int, robot_re.match(line).groups()))))

print_robots(robots)
print()

def sum_quadrants(robots):
    midx = int(COLS/2)
    midy = int(ROWS/2)
    quadrants = [0, 0, 0, 0]
    for rb in robots:
        if rb.x == midx or rb.y == midy:
            continue
        if rb.x < midx and rb.y < midy:
            quadrants[0] += 1
        elif rb.x > midx and rb.y < midy:
            quadrants[1] += 1
        elif rb.x < midx and rb.y > midy:
            quadrants[2] += 1
        elif rb.x > midx and rb.y > midy:
            quadrants[3] += 1
        else:
            print(f"unrecognized quadrant {rb}")
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

def one():
    for i in range(0, 100):
        for idx, rb in enumerate(robots):
            x = rb.x + rb.vx
            y = rb.y + rb.vy
            if x < 0:
                x += COLS
            elif x >= COLS:
                x -= COLS
            if y < 0:
                y += ROWS
            elif y >= ROWS:
                y -= ROWS
            robots[idx] = Robot((x, y, rb.vx, rb.vy))
    print_robots(robots)
    print(sum_quadrants(robots))

if args.two:
    count = 0
    while True:
        count += 1
        for idx, rb in enumerate(robots):
            x = rb.x + rb.vx
            y = rb.y + rb.vy
            if x < 0:
                x += COLS
            elif x >= COLS:
                x -= COLS
            if y < 0:
                y += ROWS
            elif y >= ROWS:
                y -= ROWS
            robots[idx] = Robot((x, y, rb.vx, rb.vy))
        print(count)
        print_robots(robots)
else:
    one()
