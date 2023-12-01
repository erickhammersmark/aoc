"""
Advent of Code day 10
https://adventofcode.com/2022/day/10
"""

import sys

input_file = "input"
if len(sys.argv) > 1 and sys.argv[1] == "sample":
    print("Using sample input data")
    input_file = "sample_input"

with open(input_file, "r") as INPUT:
    lines = [l.strip() for l in INPUT.readlines()]

"""
Part 1
Process instructions like
noop
addx 2
addx -1
Where noop takes 1 cycle, addx takes 2 cycles, and the result of addx is applied after
its two cycles have passed. Measure the value of x at the 20th cycle, then every 40 cycles
until 220. Sum up the product of the cycle (20, 60, 100...) and the value of x during that cycle.
"""

x = 1
cycle = 0
key_cycles = [20, 60, 100, 140, 180, 220]
samples = []
for line in lines:
    cycle += 1
    if cycle in key_cycles:
        samples.append(x)
    if line == "noop":
        continue
    cycle += 1
    if cycle in key_cycles:
        samples.append(x)
    x += int(line.split()[1])

sample_sum = 0
for cycle, value in zip(key_cycles, samples):
    sample_sum += cycle * value

print(f"Part 1: sum of {key_cycles} values for X register: {sample_sum}")

"""
Part 2
"""

x = 1
cycle = 0

def draw(cycle, x):
    pixel = cycle % 40
    sprite = [x-1, x, x+1]
    if pixel in sprite:
        print("#", end="")
    else:
        print(".", end="")
    if pixel == 39:
        print()

print("Part 2")
for line in lines:
    draw(cycle, x)
    cycle += 1
    if line == "noop":
        continue
    draw(cycle, x)
    cycle += 1
    x += int(line.split()[1])

