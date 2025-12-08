#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from collections import defaultdict
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    parser.add_argument("--example", action="store_true", default=False)
    parser.add_argument("--debug", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

def d(msg):
    if args.debug:
        sys.stderr.write(str(msg) + "\n")

lines = read_input(filename="example.txt" if args.example else args.filename)
board = Board(lines, filename=args.filename, example=args.example)

if args.two:
    p_locs = [(0, board[0].index("S"))]
    p_counts = [1]

    while p_locs:
        # end
        if p_locs[0][0] == len(board) - 2:
            print(sum(p_counts))
            sys.exit(0)

        # down
        for idx, p_loc in enumerate(p_locs):
            p_locs[idx] = (p_loc[0] + 1, p_loc[1])

        # split
        for idx in range(len(p_locs)):
            p_loc = p_locs[idx]
            if board.get(p_loc) == "^":
                p_locs[idx] = (p_loc[0], p_loc[1] - 1)

                p_locs.append((p_loc[0], p_loc[1] + 1))
                p_counts.append(p_counts[idx])

        # dedup
        idx = 0
        while idx < len(p_locs):
            odx = 0
            while odx < len(p_locs):
                if idx == odx:
                    odx += 1
                    continue
                if p_locs[idx] == p_locs[odx]:
                    p_counts[idx] += p_counts[odx]
                    del p_locs[odx]
                    del p_counts[odx]
                else:
                    odx += 1
            idx += 1

splits = 0
beams = [(0, lines[0].index("S"))]
for rdx, line in enumerate(lines[1:]):
    beams = list(map(lambda x: (x[0] + 1, x[1]), beams))

    bdx = 0
    while bdx < len(beams):
        beam = beams[bdx]
        if beam[1] < len(line) and line[beam[1]] == "^":
            splits += 1
            beams.remove(beam)
            if beam[1] > 0 and (beam[0], beam[1] - 1) not in beams and line[beam[1] - 1] == ".":
                beams.insert(0, (beam[0], beam[1] - 1))
                bdx += 1
            if beam[1] < len(line) - 1 and (beam[0], beam[1] + 1) not in beams and line[beam[1] + 1] == ".":
                beams.insert(0, (beam[0], beam[1] + 1))
                bdx += 1
        else:
            bdx += 1

print(splits)
