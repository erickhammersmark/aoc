#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    return parser.parse_args()

def apply(values, ranges, reverse=False):
    result = []
    for value in values:
        no_match = True
        for rng in ranges:
            if reverse:
                source, dest, length = rng
            else:
                dest, source, length = rng
            if value < source or value >= source + length:
                continue
            result.append(value - source + dest)
            no_match = False
        if no_match:
            result.append(value)
    return result

def main():
    args = parse_args()

    maps = {}
    lines = read_input()
    seeds = list(map(int, lines[0].split(": ")[1].split()))

    cmap = None
    for line in lines[2:]:
        if "map" in line:
            source, dest = line.split()[0].split("-to-")
            maps[source] = {dest: []}
            cmap = maps[source][dest]
        elif line:
            cmap.append(tuple(map(int, line.split())))

    forward = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

    values = seeds
    for n, obj in enumerate(forward):
        if obj == forward[-1]:
            break
        values = apply(values, maps[obj][forward[n+1]])
    print(min(values))

if __name__ == "__main__":
    main()
