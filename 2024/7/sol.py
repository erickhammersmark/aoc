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

operators = ("+", "*", "||")

def evaluate(equation):
    value = equation[0]
    idx = 1
    statement = [value]
    while idx < len(equation):
        if equation[idx] == "||":
            idx += 1
            value = str(value) + equation[idx]
            statement = [value]
        else:
            statement.append(equation[idx])
            if len(statement) == 3:
                value = str(eval(" ".join(statement)))
                statement = [value]
        idx += 1
    return int(value)

def try_operators(equation, test_value, operands, operators):
    if not operands:
        value = evaluate(equation)
        return value if value == test_value else 0
    if not equation:
        equation.append(operands[0])
        operands = operands[1:]
    for operator in operators:
        value = try_operators(equation + [operator, operands[0]], test_value, operands[1:], operators)
        if value:
            return value
    return 0

valid_values_sum = 0
for line in read_input(filename=args.filename):
    test_value, operands = line.split(": ")
    operands = operands.split()
    valid_values_sum += try_operators([], int(test_value), operands, operators)
print(valid_values_sum)
