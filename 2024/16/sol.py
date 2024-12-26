#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from collections import defaultdict
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

init_pos = board.find("S")
goal_pos = board.find("E")
nodes = board.find([".", "S", "E"], findall=True)
neighbors = dict((node, [n for n in board.neighbors(node) if board.clear_path(node, n)]) for node in nodes)

infinite_cost = len(board) * len(board[0]) * 1000 + board.taxi_distance(init_pos, goal_pos)
upnext = PriorityQueue(nodes, weight=infinite_cost)

costs = dict((node, infinite_cost) for node in nodes)
visited = set()
parents = dict()
dirs = dict()

curr_node = init_pos
dirs[init_pos] = (0, 1)
costs[init_pos] = 0

def print_layout(upnext):
    travelled = upnext + list((costs[vl], vl) for vl in visited)
    for row in range(0, len(board)):
        for col in range(0, len(board[0])):
            this = [(wt, vl) for wt, vl in travelled if wt != infinite_cost and vl[0] == row and vl[1] == col]
            if this:
                print(f"{this[0]}\t", end="")
            else:
                print("\t\t", end="")
        print()

"""
The bug happens when I got to a corner without turning, then explore to that corner via a shorter path, but including one more turn.
In the example4 case, the common corner at the top has a score of 3015 when approached from the bottom and the node to its left has
a score of 4008. the 4008 cell will not visit the already visited 3015 cell, and even if it would, it would not update its lower value.
One solution might be to make unique nodes per direction, or unique visited entries and costs per direction.
Another solution would be to add a new state to the walk for turning.
"""

while True:
    #print(f"Processing node {curr_node}")
    if curr_node == goal_pos:
        print(costs[curr_node])
    visited.add(curr_node)
    curr_neighbors = neighbors[curr_node][:]
    # sort straight ahead before turn and move
    #curr_neighbors.sort(key=lambda x: 0 if board.direction(curr_node, x) == dirs[curr_node] else 1)
    these_neighbors = []
    for neigh in neighbors[curr_node]:
        #if neigh in visited:
        #    continue
        neigh_cost = costs[curr_node] + 1
        neigh_dir = board.direction(curr_node, neigh)
        if neigh_dir != dirs[curr_node]:
            neigh_cost += 1000
        effective_existing_neigh_cost = costs[neigh]
        if neigh in dirs and dirs[neigh] != dirs[curr_node]:
            effective_existing_neigh_cost += 1000
        if neigh_cost < effective_existing_neigh_cost:
            parents[neigh] = curr_node
            costs[neigh] = neigh_cost
            dirs[neigh] = neigh_dir
            upnext.set(neigh, neigh_cost)
            these_neighbors.append(f"{neigh} C{neigh_cost} D{neigh_dir}")

    if not upnext:
        break

    #print_layout(upnext)

    curr_node = upnext.pop()
    curr_dir = dirs[curr_node]

    #print(f"Added neighbors: {these_neighbors}, chose next node {curr_node} D{curr_dir}")
    #input()

path = []
node = goal_pos
while node in parents:
    path.append(node)
    node = parents[node]
path.append(node)
board.print(extras=[("\u001b[31mX\033[0m", path)])
print(costs[goal_pos])
