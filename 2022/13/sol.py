"""
Advent of Code day 13
https://adventofcode.com/2022/day/13
"""

from functools import cmp_to_key
import sys

input_file = "input"
if len(sys.argv) > 1 and sys.argv[1] == "sample":
    input_file = "sample_input"

with open(input_file, "r") as INPUT:
    lines = [l.strip() for l in INPUT.readlines()]


"""
Part 1

Input are pairs of packets separated by a blank line
Each packet is an arbitrarily nested list of integers and lists of integers.
Any lists can be empty.
Find packets that are in the correct order
Compare the packets element by element
    left and right both ints: normal int comparison
    left and right are both lists: compare as with outer list
        NB: IFF there is no winner before one side runs out of elements but the other does not, left being smaller is ok, right being smaller means out of order
    if one is an int and one is a list, make the int a list and go again

What is the sum of the ordinal positions of the pairs that are in the correct order? lines 1 and 2 == 1, lines 3 and 4 == 2, etc.
"""

pairs = []
for idx in range(0, len(lines), 3):
    pairs.append((eval(lines[idx]), eval(lines[idx+1])))

def cmp_pair(left, right):
    #print(f"cmp_pair({left}, {right})")
    if type(left) == int and type(right) == int:
        if left < right:
            return 1
        if left > right:
            return -1
    elif type(left) == list and type(right) == list:
        if len(left) > len(right):
            for lv, rv in zip(left[:len(right)], right):
                val = cmp_pair(lv, rv)
                if val != 0:
                    return val
            return -1
        else:
            for lv, rv in zip(left, right[:len(left)]):
                val = cmp_pair(lv, rv)
                if val != 0:
                    return val
            if len(right) > len(left):
                return 1
    elif type(left) == list and type(right) == int:
        return cmp_pair(left, [right])
    elif type(left) == int and type(right) == list:
        return cmp_pair([left], right)

    return 0

correct_pairs = []
for idx, pair in enumerate(pairs):
    val = cmp_pair(*pair)
    if val == 1:
        correct_pairs.append(idx+1)

print(correct_pairs)
print(f"Part 1: {sum(correct_pairs)}")

"""
Part 2

Sort all packets into correct order, disregarding pairs.
Also insert two divider packets, [[2]] and [[6]].
multiply the 1-based indices of the divider packets.
"""

all_packets = []
for pair in pairs:
    all_packets.extend(list(pair))
dividers = [[[2]], [[6]]]
all_packets.extend(dividers)

all_packets.sort(key=cmp_to_key(lambda x, y: 0 - cmp_pair(x, y)))
decoder_key = 1
for idx, packet in enumerate(all_packets):
    if packet in dividers:
        decoder_key *= idx + 1

print(f"Part 2: {decoder_key}")
