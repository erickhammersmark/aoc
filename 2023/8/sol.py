#!/usr/bin/env python

import math
import sys

from argparse import ArgumentParser

sys.path.append("..")
from lib import read_input

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

lines = read_input(filename=args.filename)

ops = lines[0]

tree = {}
for line in lines[2:]:
    tree[line[0:3]] = [line[7:10], line[12:15]]

def traverse(node, end):
    count = 0
    while True:
        for op in (0 if o == "L" else 1 for o in ops):
            count += 1
            node = tree[node][op]
            if node.endswith(end):
                return count

if args.two:
    print(math.lcm(*(traverse(node, "Z") for node in tree.keys() if node.endswith("A"))))
else:
    print(traverse("AAA", "ZZZ"))
