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


X=0
Y=1
COST=2

machines = []
A = None
B = None
P = None
for line in read_input(filename=args.filename):
    if A and B and P:
        machines.append((A, B, P))
        A = None
        B = None
        P = None
    if not line:
        continue
    name, values = line.split(": ")
    values = list(map(int, values.replace("X","").replace("Y","").replace("=","").split(", ")))
    if name == "Button A":
        A = (*values, 3)
    elif name == "Button B":
        B = (*values, 1)
    elif name == "Prize":
        if args.two:
            P = tuple([v + 10000000000000 for v in values])
        else:
            P = tuple(values)
    else:
        raise Exception(f"Unknown value name: {name} from line {line}")
else:
    machines.append((A, B, P))

"""
Each machine's A and B buttons offer different values in each direction. One may favor multiple
presses of B to achieve the same result as one press of A, others may heavily favor minimizing
use of B to accomplish the task using fewer, more effecient As.

First step must be to find if there are any pairs of button presses that will reach the prize.
The prize's location in each direction must be itself or by a sum of two numbers divisible by
one or both of the button values in that direction. The individual case is trivial. To find if
the prize's X or Y location can be reached by a sum of multiples of each of the buttons' X or Y
values is harder. The limit of 100 button presses makes a brute force approach reasonable, but
this style of approach often must be discarded for part 2 of a puzzle like this.

Edit: told you.

Rewriting the whole thing do just do algebra. O(n^2) -> O(1)

Ap * A[X] + Bp * B[X] = P[X]
Ap * A[X] = P[X] - Bp * B[X]
Ap = (P[X] - Bp * B[X]) / A[X]

Ap * A[Y] + Bp * B[Y] = P[Y]
((P[X] - Bp * B[X]) / A[X]) * A[Y] + Bp * B[Y] = P[Y]
( (P[X] - Bp * B[X]) * (1 / A[X]) ) * A[Y] + Bp * B[Y] = P[Y]
( P[X] / A[X] - Bp * B[X] / A[X] ) * A[Y] + Bp * B[Y] = P[Y]
A[Y] * P[X] / A[X] - Bp * B[X] * A[Y] / A[X] + Bp * B[Y] = P[Y]
A[Y] * P[X] / A[X] - P[Y] = Bp * B[X] * A[Y] / A[X] - Bp * B[Y]
A[Y] * P[X] / A[X] - P[Y] = Bp * (B[X] * A[Y] / A[X] - B[Y])
(A[Y] * P[X] / A[X] - P[Y]) / (B[X] * A[Y] / A[X] - B[Y]) = Bp
"""

def rnd(val):
    if val - int(val) > 0.001 and val - int(val) < 0.999:
        return (val, False)
    presses = round(val)
    return (presses, True)

def solve(machine, limit=100):
    A, B, P = machine
    Bp, Bok = rnd((A[Y] * P[X] / A[X] - P[Y]) / (B[X] * A[Y] / A[X] - B[Y]))
    Ap, Aok = rnd((P[X] - Bp * B[X]) / A[X])
    if not Aok or not Bok or Ap < 0 or Bp < 0 or (limit and (Ap > limit or Bp > limit)):
        forward = (-1, -1, 0)
    else:
        forward = (Ap, Bp, Ap * A[COST] + Bp * B[COST])
    Ap, Aok = rnd((B[Y] * P[X] / B[X] - P[Y]) / (A[X] * B[Y] / B[X] - A[Y]))
    Bp, Bok = rnd((P[X] - Ap * A[X]) / B[X])
    if not Aok or not Bok or Ap < 0 or Bp < 0 or (limit and (Ap > limit or Bp > limit)):
        backward = (-1, -1, 0)
    else:
        backward = (Ap, Bp, Ap * A[COST] + Bp * B[COST])
    if forward[2] == 0:
        return backward
    if backward[2] == 0:
        return forward
    if forward[2] < backward[2]:
        return forward
    return backward

def one(limit=100):
    total_cost = 0
    for machine in machines:
        solve_result = solve(machine, limit=limit)
        total_cost += solve_result[2]
    return total_cost

def two():
    return one(limit=0)

if args.two:
    print(two())
else:
    print(one())
