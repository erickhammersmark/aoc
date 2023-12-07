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

cardrank = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

if args.two:
    cardrank["J"] = 1

HT_FIVE = 7
HT_FOUR = 6
HT_FULL = 5
HT_THREE = 4
HT_TWO = 3
HT_ONE = 2
HT_HIGH = 1
HT_UNKNOWN = 0

def handtype(orig_hand):
    hand = orig_hand[:]
    hand.sort(key=lambda x: 0-x)
    ht = HT_UNKNOWN
    groups = []
    J = 0
    for val in hand:
        if args.two and val == 1:
            J += 1
            continue
        if groups and groups[-1] and val == groups[-1][0]:
            groups[-1].append(val)
        else:
            groups.append([val])
    groups.sort(key=lambda x: 0-len(x))
    if args.two and J:
        if not groups:
            groups.append([])
        groups[0].extend([1] * J)
    if len(groups[0]) == 5:
        ht = HT_FIVE
    elif len(groups[0]) == 4:
        ht = HT_FOUR
    elif len(groups[0]) == 3:
        if len(groups) == 2:
            ht = HT_FULL
        elif len(groups) == 3:
            ht = HT_THREE
    elif len(groups[0]) == 2:
        if len(groups[1]) == 2:
            ht = HT_TWO
        elif len(groups) == 4:
            ht = HT_ONE
    elif len(groups) == 5:
        ht = HT_HIGH
    #for idx, d in enumerate([d for group in groups for d in group]):
    #    hand[idx] = d
    return ht

def handrank(hand):
    digits = [handtype(hand), *hand]
    return int(''.join(map(lambda x: f"{x:02d}", digits)))

def handcmp(a, b):
    return handrank(a) > (b)

data = []
for line in read_input():
    hand, bid = line.split()
    hand = list(map(lambda x: cardrank[x], hand))
    data.append(tuple((hand, int(bid))))
data.sort(key = lambda x: handrank(x[0]))
for datum in data:
    print(datum)

print(sum((idx + 1) * handbid[1] for idx, handbid in enumerate(data))) 
