#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from functools import reduce
from lib import *

T = 0
D = 1

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    return parser.parse_args()

def calc_dist(hold_time, tot_time):
    travel_time = tot_time - hold_time
    return hold_time * travel_time

def does_it_win(race, hold_time):
    return calc_dist(hold_time, race[T]) > race[D]

def main():
    args = parse_args()
    data = []
    lines = read_input(filename=args.filename)
    for time in map(int, lines[0].split()[1:]):
        data.append([time])
    for idx, dist in enumerate(map(int, lines[1].split()[1:])):
        data[idx].append(dist)

    wins = []
    for race in data:
        # holding for 0 or the whole time can never win
        wins.append(0)
        for hold_time in range(1, race[T]):
            if does_it_win(race, hold_time):
                wins[-1] += 1
    print( reduce(lambda x, y: x * y, wins) )

if __name__ == "__main__":
    main()
