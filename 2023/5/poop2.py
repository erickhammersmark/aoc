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
        value_result = apply_one(value, ranges, reverse=reverse)
        if value_result == []:
            value_result = [value]
        result.extend(value_result)
    return result

def apply_one(value, ranges, reverse=False):
    result = []
    for rng in ranges:
        if reverse:
            source, dest, length = rng
        else:
            dest, source, length = rng
        if value < source or value >= source + length:
            continue
        result.append(value - source + dest)
    return result

def main():
    args = parse_args()

    maps = {}
    lines = read_input()
    seeds = list(map(int, lines[0].split(": ")[1].split()))
    maps["seeds"] = []
    for n in range(0, len(seeds), 2):
        maps["seeds"].append(tuple(map(int, (seeds[n], seeds[n], seeds[n+1]))))

    cmap = None
    for line in lines[2:]:
        if "map" in line:
            source, dest = line.split()[0].split("-to-")
            maps[source] = {dest: []}
            cmap = maps[source][dest]
        elif line:
            cmap.append(tuple(map(int, line.split())))

    forward = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
    reverse = forward[:]
    print(reverse)
    reverse.reverse()

    values = maps["humidity"]["locations"]
    for location in values[:]:
        values = [location]
        for n, obj in enumerate(reverse):
            if obj == reverse[-2]:
                break
        values = apply(values, maps[reverse[n+1][obj]])
        print(obj, maps[obj].values())
    print(min(values))

if __name__ == "__main__":
    main()
