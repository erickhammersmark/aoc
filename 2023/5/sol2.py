#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

BASE=0
LEN=1

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    return parser.parse_args()

def overlap(val_rng, rng):
    val_max = val_rng[BASE] + val_rng[LEN] - 1
    range_max = rng[BASE] + rng[LEN] - 1

    if any((
        val_max < rng[BASE],
        range_max < val_rng[BASE],
        val_rng[BASE] > range_max,
        rng[BASE] > val_max
    )):
        return ()

    start = max(val_rng[BASE], rng[BASE])
    end = min(val_max, range_max)
    length = 1 + end - start
    return (start, length)

def apply_range(val_rng, rng):
    dest, source, length = rng
    ol = overlap(val_rng, (source, length))
    if not ol:
        return ol
    return (ol[BASE] - source + dest, ol[LEN])

def apply_ranges(val_ranges, ranges):
    result = []
    for val_rng in val_ranges:
        for rng in ranges:
            val_rng_result = apply_range(val_rng, rng)
            if val_rng_result:
                result.append(val_rng_result)
    return result

def main():
    args = parse_args()

    lines = read_input()
    seeds = list(map(int, lines[0].split(": ")[1].split()))
    seed_ranges = []
    for n in range(0, len(seeds), 2):
        seed_ranges.append((seeds[n], seeds[n+1]))

    maps = {}
    cmap = None
    for line in lines[2:]:
        if "map" in line:
            source, dest = line.split()[0].split("-to-")
            maps[source] = []
            cmap = maps[source]
        elif line:
            cmap.append(tuple(map(int, line.split())))

    forward = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

    values = seed_ranges
    for n, obj in enumerate(forward):
        if obj == forward[-1]:
            break
        values = apply_ranges(values, maps[obj])
    print(min(value[0] for value in values))

if __name__ == "__main__":
    main()
