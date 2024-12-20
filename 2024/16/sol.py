#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from copy import copy
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    parser.add_argument("--example", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

lines = read_input(filename="example.txt" if args.example else args.filename)
board = Board(lines, filename=args.filename, example=args.example)
sys.setrecursionlimit(len(board) * len(board[0]))

class Node(object):
    def __init__(self, pos, _dir):
        self.val = board.get(pos)
        self.pos = pos
        self.dir = _dir
        self.children = [] # (cost [including turn], pos, new direction if you move there)
        for neigh in board.neighbors(self.pos, diagonal=False):
            neigh_val = board.get(neigh)
            if neigh_val == "#":
                continue
            if neigh_val in [".", "E"]:
                neigh_dir = board.direction(self.pos, neigh)
                cost = 1001
                if neigh_dir == self.dir:
                    cost = 1
                self.children.append({"cost":cost, "pos":neigh, "dir":neigh_dir})
        self.children.sort(key=lambda c:c["cost"])
    def __str__(self):
        return f"Node {self.pos} ({self.val}) dir {self.dir} kids:{self.children}"

def walk(node, visited, results, cost):
    #print(f"walk({node}, {visited}, {results}, {cost}")
    if node.val == "E":
        return results.append((cost, visited[:]))
    lowest_cost = 1001 * len(board) * len(board[0])
    if results:
        lowest_cost = min(result[0] for result in results)
    for child in node.children:
        if child["pos"] in visited:
            continue
        if cost + child["cost"] > lowest_cost:
            continue
        if cost + child["cost"] > 67500:
            continue
        walk(Node(child["pos"], child["dir"]), visited + [child["pos"]], results, cost + child["cost"])

init_pos = board.find("S")
pos = init_pos
results = []
walk(Node(init_pos, (0, 1)), [init_pos], results, 0)
results.sort()
print(results[0][0])
#board.print(extras=[("X", [(0,0),(1,1),(2,2),(3,3)])])
