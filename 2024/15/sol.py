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

lines = read_input(filename="example.txt" if args.example else args.filename)
#board = Board(lines, filename=args.filename, example=args.example)

movemap = { "<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0) }

b = []
moves = ""
bflag = True
for line in lines:
    if line == "":
        bflag = False
    if bflag:
        if args.two:
            line = line.replace(".", "..").replace("O", "[]").replace("#", "##").replace("@", "@.")
        b.append(line)
    else:
        moves = moves + line.rstrip()
board = Board(b)

def box_value(pos):
    return 100 * pos[0] + pos[1]

def sum_boxes():
    _sum = 0
    for idx, row in enumerate(board):
        for col, val in enumerate(row):
            if val == "O" or val == "[":
                _sum += box_value((idx, col))    
    return _sum

def can_move(pos, _dir):
    target = tuple(p + d for p, d in zip(pos, _dir))
    if board.oob(target):
        return (pos, False)
    target_val = board.get(target)
    if target_val == "#":
        return False
    if target_val == ".":
        return True
    if target_val == "O":
        return can_move(target, _dir)
    if target_val == "[":
        if _dir == (0, -1):
            return can_move(target, _dir)
        if _dir == (0, 1):
            return can_move(target, _dir)
        if _dir[0] != 0:
            # up or down
            left_ok = can_move(target, _dir)
            right_ok = can_move((target[0], target[1]+1), _dir)
            if left_ok and right_ok:
                return True
            return False
    if target_val == "]":
        if _dir == (0, 1):
            return can_move(target, _dir)
        if _dir == (0, -1):
            return can_move(target, _dir)
        if _dir[0] != 0:
            # up or down
            right_ok = can_move(target, _dir)
            left_ok = can_move((target[0], target[1]-1), _dir)
            if left_ok and right_ok:
                return True
            return False
    raise Exception(f"Unknown board charcter: {target_val} at {target}")

def try_move(pos, _dir):
    target = tuple(p + d for p, d in zip(pos, _dir))
    if board.oob(target):
        return (pos, False)
    target_val = board.get(target)
    if target_val == "#":
        return (pos, False)
    if target_val == ".":
        board.set(target, board.get(pos))
        board.set(pos, ".")
        return (target, True)
    if target_val == "O":
        result, ok = try_move(target, _dir)
        if ok:
            board.set(target, board.get(pos))
            board.set(pos, ".")
            return (target, True)
        return (pos, False)
    if target_val == "[":
        if _dir == (0, -1):
            result, ok = try_move(target, _dir)
            if ok:
                board.set(target, "]")
                return (target, True)
            return (pos, False)
        if _dir == (0, 1):
            result, ok = try_move(target, _dir)
            if ok:
                board.set(target, board.get(pos))
                board.set(pos, ".")
                return (target, True)
            return (pos, False)
        if _dir[0] != 0:
            # up or down
            if can_move(target, _dir) and can_move((target[0], target[1]+1), _dir):
                left_result, left_ok = try_move(target, _dir)
                right_result, right_ok = try_move((target[0], target[1]+1), _dir)
                if left_ok and right_ok:
                    board.set(target, board.get(pos))
                    board.set(pos, ".")
                    return (target, True)
            return (pos, False)
    if target_val == "]":
        if _dir == (0, 1):
            result, ok = try_move(target, _dir)
            if ok:
                board.set(target, "[")
                return (target, True)
            return (pos, False)
        if _dir == (0, -1):
            result, ok = try_move(target, _dir)
            if ok:
                board.set(target, board.get(pos))
                board.set(pos, ".")
                return (target, True)
            return (pos, False)
        if _dir[0] != 0:
            # up or down
            if can_move(target, _dir) and can_move((target[0], target[1]-1), _dir):
                right_result, right_ok = try_move(target, _dir)
                left_result, left_ok = try_move((target[0], target[1]-1), _dir)
                if left_ok and right_ok:
                    board.set(target, board.get(pos))
                    board.set(pos, ".")
                    return (target, True)
            return (pos, False)
    raise Exception(f"Unknown board charcter: {target_val} at {target}")

init_pos = board.find("@")
pos = init_pos
for move in moves:
    _dir = movemap[move]
    board.set(pos, ".")
    pos, ok = try_move(pos, _dir)
    board.set(pos, "@")
board.print()
print(sum_boxes())
