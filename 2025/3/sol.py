#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    parser.add_argument("--example", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

num_bats = 2
if args.two:
    num_bats = 12

lines = read_input(filename="example.txt" if args.example else args.filename)

joltages = []

def fits(digits, idx, q):
    distance_from_goal = num_bats - len(q)
    remaining_digits = len(digits) - idx
    return remaining_digits >= distance_from_goal

for line in lines:
    digits = list(map(int, line))
    def v(i):
        return digits[i]
    q = []
    for idx, digit in enumerate(digits):
        #print(f"idx: {idx}, digit: {v(idx)}, q: {list(map(v, q))}")
        while q and digit > v(q[-1]) and fits(digits, idx, q[:-1]):
            q.pop(-1)
        if len(q) < num_bats:
            q.append(idx)
    joltage = 0
    power = 1
    for j_dig in reversed(list(map(v, q))):
        joltage += j_dig * power
        power *= 10
    joltages.append(joltage)

print(joltages)
print(sum(joltages))
