#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from functools import reduce
from lib import *


class Rng(object):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __contains__(self, other):
        if type(other) == int:
            return self.low <= other <= self.high

        if type(other) == Rng:
            return other.low in self or other.high in self

    def __len__(self):
        return 1 + self.high - self.low

    def merge(self, rng):
        if rng in self or self in rng:
            low = min(self.low, rng.low)
            high = max(self.high, rng.high)
            return Rng(low, high)
        return None

    def __repr__(self):
        return f"{self.low}-{self.high}"


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    parser.add_argument("--example", action="store_true", default=False)
    parser.add_argument("--debug", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

def d(msg):
    if args.debug:
        sys.stderr.write(str(msg) + "\n")

lines = read_input(filename="example.txt" if args.example else args.filename)

ranges = []
ingredients = set()
for line in lines:
    if not line:
        continue
    if "-" in line:
        ranges.append(Rng(*map(int, line.split("-"))))
    else:
        for rng in ranges:
            if int(line) in rng:
                ingredients.add(line)

if not args.two:
    print(len(ingredients))
    sys.exit()

for rng in ranges:
    d(rng)

any_merged = True
while any_merged:
    any_merged = False
    idx = 0
    while idx < len(ranges):
        cur = ranges[idx]
        odx = idx

        d(f"idx: {idx}, cur: {cur}")

        while odx < len(ranges):
            if idx == odx:
                odx += 1
                continue
            other = ranges[odx]

            d(f"odx: {odx}, other: {other}")

            if other in cur or cur in other:
                d(f"overlap detected")

                cur = cur.merge(other)

                d(f"new range: {ranges[idx]}")
                d(f"removing range: {other}")

                ranges.remove(other)
                ranges[idx] = cur
                any_merged = True
            odx += 1
        idx += 1

print(sum(map(len, ranges)))
