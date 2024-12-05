#!/usr/bin/env python

import functools
import sys
sys.path.append("..")

from argparse import ArgumentParser
from collections import defaultdict
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

rules = defaultdict(list) # use second page as key, first page as element in value list
jobs = []
for line in read_input(filename=args.filename):
    if "|" in line:
        _prev, _next = line.split("|")
        rules[_next].append(_prev)
    elif line != "":
        jobs.append(line.split(","))

def rulecmp(a, b):
    if a in rules and b in rules[a]:
        return -1
    elif b in rules and a in rules[b]:
        return 1
    else:
        return 0

total = 0
for job in jobs:
    seen_pages = set()
    valid = True
    for page in job:
        seen_pages.add(page)
        if page in rules:
            for _p in rules[page]:
                if _p not in job:
                    continue
                if _p not in seen_pages:
                    valid = False
                    break # for _p in rules[page]
        if not valid:
            break # for page in job

    if args.two:
        if valid:
            continue # for job in jobs
        job.sort(key=functools.cmp_to_key(rulecmp))
        valid = True

    if valid:
        mid_idx = int(len(job)/2)
        total += int(job[mid_idx])

print(total)
