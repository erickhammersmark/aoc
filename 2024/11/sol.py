#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

from functools import cache

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

stones = list(map(int, read_input(filename=args.filename)[0].split()))

stone_cache = {}

@cache
def apply_one_rules(stone):
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        midpoint = int(len(stone_str)/2)
        left = int(stone_str[:midpoint])
        right = int(stone_str[midpoint:])
        return [left, right]
    return [stone * 2024]

def apply_two_rules(stones, final_boss=False):
    new_stones = []
    count = 0
    for stone in stones:
        if stone in stone_cache:
            if final_boss:
                count += len(stone_cache[stone])
            else:
                new_stones.extend(stone_cache[stone])
        else:
            calculated_stones = one([stone])
            if final_boss:
                count += len(calculated_stones)
            else:
                new_stones.extend(calculated_stones)
                stone_cache[stone] = calculated_stones
    if final_boss:
        return count
    return new_stones

def one(stones):
    for _ in range(0, 25):
        new_stones = []
        for stone in map(apply_one_rules, stones):
            new_stones.extend(stone)
        stones = new_stones
    return stones

def two(stones):
    result = 0
    for stone in stones:
        print(f"Processing {stone}")
        stones25 = apply_two_rules([stone], final_boss=False)
        print(f"25: {len(stones25)}")
        stones50 = apply_two_rules(stones25, final_boss=False)
        print(f"50: {len(stones50)}")
        stones75 = apply_two_rules(stones50, final_boss=True)
        print(f"75: {stones75}")
        result += stones75
    print(result)

if args.two:
    two(stones)
else:
    print(len(one(stones)))
