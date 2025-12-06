#!/usr/bin/env python

import sys
from argparse import ArgumentParser
from functools import reduce

sys.path.append("..")
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
#board = Board(lines, filename=args.filename, example=args.example)

def operator_func(operator):
    if operator == "+":
        return lambda x, y: x + y
    if operator == "*":
        return lambda x, y: x * y
    if operator == "-":
        return lambda x, y: x - y
    if operator == "/":
        return lambda x, y: x / y
    return lambda x, y: x, y

def p2_parse_line(line):
    line = line.strip()
    if not line:
        return (None, None)
    if not any(op in line for op in ["+", "*"]):
        return (int(line), None)
    return (int(line[:-1]), operator_func(line[-1]))

if args.two:
    """
    123 328  51 64 
     45 64  387 23 
      6 98  215 314
    *   +   *   +  

    becomes

    4 + 431 + 623
    175 + 581 + 32
    8 + 248 + 369
    356 * 24 * 1

    ROTATE the lines array CCW
        small ROW becomes small COL
        big ROW becomes big COL
        small COL becomes big ROW
        big COL becomes small ROW

    each line forms a digit
    when the line ends with + or *, the expression is done
    """

    new_row_count = max(map(len, lines))
    rot_lines = [[] for _ in range(new_row_count)]

    for line in lines:
        for rdx in range(new_row_count-1, -1, -1):
            char = line[rdx] if rdx < len(line) else " "
            rot_lines[new_row_count - 1 - rdx].append(char)

    digits = []
    count = 0
    for line in rot_lines:
        line = "".join(line)
        digit, oper = p2_parse_line(line)
        if not digit:
            continue
        digits.append(digit)
        if oper:
            count += reduce(oper, digits)
            digits = []

    print(count)
    sys.exit(0)


columns = []
operators = []

for line in lines:
    if any(op in line for op in ["+", "*"]):
        operators = line.split()
    else:
        columns.append(list(map(int, line.split())))

operands = []
for dummy in range(0, len(operators)):
    operands.append([])

for rdx, row in enumerate(columns):
    for cdx, operand in enumerate(row):
        operands[cdx].append(operand)

count = 0
for idx, col in enumerate(operands):
    count += reduce(operator_func(operators[idx]), col)

print(count)
