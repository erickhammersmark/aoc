"""
Advent of Code day X
https://adventofcode.com/2022/day/X
"""

import sys

input_file = "input"
if len(sys.argv) > 1 and sys.argv[1] == "sample":
    input_file = "sample_input"

with open(input_file, "r") as INPUT:
    lines = [l.strip() for l in INPUT.readlines()]


