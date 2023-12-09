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

def extrapolate(line):
    # I don't HAVE to keep all of all of them, only have to keep all of the last one, but w/e
    deltas = [list(map(int, line.split()))]
    if args.two:
        deltas[-1].reverse()
    while not all(d == 0 for d in deltas[-1]):
        deltas.append([])
        for idx, num in enumerate(deltas[-2][1:]):
            deltas[-1].append(num - deltas[-2][idx])
    return sum(itr[-1] for itr in deltas)

print(sum((extrapolate(line) for line in read_input(filename=args.filename))))
