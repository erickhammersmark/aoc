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

def is_safe(report, two=False):
    values = report.split()
    if two:
        pos = 0
        while pos < len(values):
            if is_safe(" ".join(values[:pos] + values[pos+1:]), two=False):
                return True
            pos += 1
    values = list(map(int, values))

    if len(values) < 2:
        raise(Exception("EINVAL"))

    if values[1] - values[0] > 0:
        direction = True
    elif values[1] - values[0] < 0:
        direction = False
    else:
        return False

    pos = 0
    while pos < len(values) - 1:
        pos += 1
        delta = values[pos] - values[pos - 1]

        if delta == 0:
            return False

        if abs(delta) > 3:
            return False

        if delta > 0 and direction:
            continue

        if delta < 0 and not direction:
            continue

        return False

    return True

reports = read_input(filename=args.filename)

safe_count = 0

for report in reports:
    if is_safe(report, two=args.two):
        safe_count += 1

print(safe_count)
