#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--example", action="store_true", default=False)
    return parser.parse_args()

def test_pat(pat, strid):
    if len(strid) % len(pat):
        return False
    if strid.count(pat) * len(pat) == len(strid):
        return True
    return False

args = parse_args()

line = read_input(filename="example.txt" if args.example else args.filename, oneline=True)
spans = tuple(tuple(map(int, span.split("-"))) for span in line.split(","))
badids_partone = []
badids_parttwo = []

for low, high in spans:
    for id in range(low, high+1):
        strid = str(id)
        half = int(len(strid)/2)
        if strid[:half] == strid[half:]:
            badids_partone.append(strid)
        for end in range(1, half+1):
            if test_pat(strid[0:end], strid):
                badids_parttwo.append(strid)
                break
print(f"Part one: {sum(map(int, badids_partone))}")
print(f"Part two: {sum(map(int, badids_parttwo))}")

