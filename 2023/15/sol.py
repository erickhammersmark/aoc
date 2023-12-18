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

def hash(orig):
    val = 0
    for char in orig:
        val += ord(char)
        val *= 17
        val %= 256
    return val

text = ''.join(read_input(filename=args.filename)).split(",")

if args.two:
    boxes = [[] for x in range(256)]

    for stepno, step in enumerate(text):
        if "-" in step:
            op_pos = step.index("-")
        else:
            op_pos = step.index("=")

        label = step[:op_pos]
        box = hash(label)
        op = step[op_pos]

        focal_length = 0
        if op == "=":
            focal_length = int(step[op_pos+1:])

        #print(f"Step {stepno}: {step}, label {label}, box {box}, op {op}, focal_length {focal_length}")

        if op == "-":
            for idx, l in enumerate(boxes[box]):
                if l[0] == label:
                    del(boxes[box][idx])
                    break

        elif op == "=":
            lens = (label, focal_length)
            for idx, l in enumerate(boxes[box]):
                if l[0] == label:
                    boxes[box][idx] = lens
                    break
            else:
                boxes[box].append(lens)
        else:
            print(f"Unknown op: {op}")
    
    total_power = 0
    for idx, box in enumerate(boxes):
        for lidx, lens in enumerate(box):
            total_power += (idx + 1) * (lidx + 1) * lens[1]
    print(total_power)

else:
    print(sum(hash(word) for word in text))

