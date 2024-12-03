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

state = None
dostate = None
dontstate = None
first = None
second = None

result = 0

enabled = True

for c in "".join(read_input(filename=args.filename)):
    if args.two:
        if c == "d" and dostate is None and dontstate is None:
            dostate = "d"
            dontstate = "d"
        elif c == "o" and dostate == "d" and dontstate == "d":
            dostate = "o"
            dontstate = "o"
        elif c == "n" and dontstate == "o":
            dostate = None
            dontstate = "n"
        elif c == "\'" and dontstate == "n":
            dontstate = "'"
        elif c == "t" and dontstate == "'":
            dontstate = "t"
        elif c == "(" and dontstate == "t":
            dontstate = "("
        elif c == ")" and dontstate == "(":
            enabled = False
            dontstate = None
        elif c == "(" and dostate == "o":
            dontstate = None
            dostate = "("
        elif c == ")" and dostate == "(":
            enabled = True
            dostate = None
        else:
            dostate = None
            dontstate = None

    if not enabled:
        continue

    if c == "m" and state == None:
        state = "m"
    elif c == "u" and state == "m":
        state = "u"
    elif c == "l" and state == "u":
        state = "l"
    elif c == "(" and state == "l":
        state = "first"
        first = None
    elif c >= "0" and c <= "9" and state == "first":
        if first is None:
            first = int(c)
        else:
            first = first * 10 + int(c)
    elif c == "," and state == "first" and first is not None:
        state = "second"
        second = None
    elif c >= "0" and c <= "9" and state == "second":
        if second is None:
            second = int(c)
        else:
            second = second * 10 + int(c)
    elif c == ")" and state == "second" and second is not None:
        result += first * second
        state = None
        first = None
        second = None
    else:
        state = None
        first = None
        second = None

print(result)
