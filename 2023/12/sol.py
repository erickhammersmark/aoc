#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from functools import cache
from lib import *
from multiprocessing import Pool


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    parser.add_argument("--poolsize", type=int, default=8)
    return parser.parse_args()

args = parse_args()


def brute_force_count_groups(springs, checksums):
    """
    Idea is to generate all possible ways to replace the ? with # or .
    and see which ones make the right groups in the right order.
    """
    num_qms = springs.count("?")
    binary_strings = [f"{n:0{num_qms}b}".replace("0", ".").replace("1", "#") for n in range(0, 2**num_qms)]
    count = 0
    for bs in [list(b) for b in binary_strings]:
        potential_solution = []
        for char in springs:
            if char == "?":
                potential_solution.append(bs.pop(0))
            else:
                potential_solution.append(char)
        if [len(group) for group in filter(lambda x: x, ''.join(potential_solution).split("."))] == checksums:
            count += 1
    return count

@cache
def count_groups(springs, checksums, mid_group = False):
    #print(f"count_groups({springs}, {checksums}, mid_group = {mid_group}")
    """
    Use the characters in springs to use up the counts in checksums.

    Every time we have a choice about whether or not to start using up a new checksum,
    also branch to not start the checksum there. In this case, return the sum of both operations.
    The call that consumes the current "?" should decrement checksums[0] and call again with the next
    substring of springs and the mid_group flag True.
    The call that passes on the current "?" should leave checksums[0] alone and call again with the next
    substring of springs and the mid_group flag absent.

    If this call contains an empty checksums and springs with no more "#" in it, return 1.
    If this call finds that we have encountered a "." while mid_group is True and checksums[0] is non-zero, return 0.
    If this call finds a "." while mid_group is True and checksums[0] is zero, return a recursive call with springs[1:] and checksums[1:]
    if this call finds a "#" while mid_group is True and checksums[0] is zero, return 0.
    If this call finds a "?" while mid_group is True and checksums[0] is zero, return a recursive call with springs[1:] and checksums[1:]
    If this call finds a "?" while mid_group is True and checksums[0] is not zero, decrement checksums[0] and return a recursive call with springs[1:] and checksums
    If this call finds a "?" while mid_group is False, branch as above.
    
    """
    checksums = list(checksums[:])

    if not checksums:
        if "#" in springs:
            return 0
        return 1

    if springs.count("#") + springs.count("?") < sum(checksums):
        return 0

    if not springs:
        if any(csum for csum in checksums):
            return 0
        return 1

    if springs[0] == ".":
        if mid_group:
            if checksums[0] == 0:
                return count_groups(springs[1:], tuple(checksums[1:]))
            else:
                return 0
        else:
            return count_groups(springs[1:], tuple(checksums))

    if springs[0] == "#":
        if mid_group:
            if checksums[0] == 0:
                return 0
            else:
                checksums[0] -= 1
                return count_groups(springs[1:], tuple(checksums), mid_group=True)
        else:
            if checksums[0]:
                checksums[0] -= 1
                return count_groups(springs[1:], tuple(checksums), mid_group=True)
            else:
                return 0

    if springs[0] == "?":
        if mid_group:
            if checksums[0]:
                checksums[0] -= 1
                return count_groups(springs[1:], tuple(checksums), mid_group=True)
            else:
                return count_groups(springs[1:], tuple(checksums[1:]))
        else:
            return count_groups(springs[1:], tuple([checksums[0] - 1] + checksums[1:]), mid_group=True) + count_groups(springs[1:], tuple(checksums))



def process_line(arg):
    idx, line = arg
    springs, checksums = line.split()
    checksums = list(map(int, checksums.split(",")))
    if args.two:
        springs = "?".join((springs, springs, springs, springs, springs))
        checksums = 5 * checksums
    #springs = [grp for grp in springs.split(".") if grp]
    line_count = count_groups(springs, tuple(checksums))
    print(f"line {idx+1}/1000: {line}, count {line_count}")
    return line_count


mp_args = [[idx, line] for idx, line in enumerate(read_input(filename=args.filename))]
with Pool(args.poolsize) as mp_pool:
    sums = mp_pool.map(process_line, mp_args)

print(sum(sums))
