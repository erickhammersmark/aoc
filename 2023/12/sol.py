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

"""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

def count_groups(springs, checksums):
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

def old_count_groups(springs, checksums):
    """
    Walk the input springs, looking for anywhere where checksums[0] fits
    Whereever it fits, put it there, then pass the rest of the springs and checksum[1:] to another call
    If checksum[1:] is empty, just return 1
    Otherwise, return whatever the other call returns
    """
    springs = springs[:]
    checksum = checksums[:]

    #print(f"count_groups({springs}, {checksums})")
    # can't make any more if one or the other is empty
    if not springs or not checksums:
        return 0

    # pop whole, in-order matches off the front and back
    while springs and checksums and "?" not in springs[0] and len(springs[0]) == checksums[0]:
        springs.pop(0)
        checksums.pop(0)
    if not checksums:
        return 1
    if not springs:
        return 0

    while springs and checksums and "?" not in springs[-1] and len(springs[-1]) == checksums[-1]:
        springs.pop(-1)
        checksums.pop(-1)
    if not checksums:
        return 1
    if not springs:
        return 0

    # any group that cannot fit any of the checksums can never change
    for idx, grp in enumerate(springs):
        if all(len(grp) < csum for csum in checksums):
            del springs[idx]

    if not springs:
        return 0

    # any leading group that cannot fit the first checksum can never change
    while springs and len(springs[0]) < checksums[0]:
        springs.pop(0)

    if not springs:
        return 0
   
    # now we know that the first group can fit the first chcksum
    while springs and "?" not in springs[0]:
        if len(springs[0]) == checksums[0]:
            springs.pop(0)
            checksums.pop(0)
        else:
            return 0

    if not springs and not checksums:
        return 1

    if not springs:
        return 0

    if not checksums:
        return 1

    count = 0

    # springs[0] can fit checksums[0] and it has some ? in it
    group = springs[0]
    csum = checksums[0]
    for idx in range(0, len(group) - csum + 1):
        # try all the possibilities in springs[0] to fit checksums[0] characters
        if idx + csum <= len(group)-1 and group[idx+csum] == "#":
            # can't start at idx, group would be too long
            continue
        if idx > 0 and group[idx-1] == "#":
            # can't start at idx, group would be too long
            continue
        if idx + csum < len(group)-1:
            tmp_group = [group[idx+csum+1:]]
        else:
            tmp_group = []
        if len(checksums) == 1:
            if all("#" not in grp for grp in [tmp_group] + springs[1:]):
                # no more checksums to apply, no unaccounted for #, this is a solution
                count += 1
                #print(f"Incr count to {count}")
            else:
                continue
        else:
            new_count = count_groups(tmp_group + springs[1:], checksums[1:])
            count += new_count
            #print(f"Recursion count {new_count}, total {count}")

    return count


total_count = 0
for idx, line in enumerate(read_input(filename=args.filename)):
    springs, checksums = line.split()
    checksums = list(map(int, checksums.split(",")))
    if args.two:
        springs = "?".join((springs, springs, springs, springs, springs))
        checksums = 5 * checksums
    #springs = [grp for grp in springs.split(".") if grp]
    line_count = count_groups(springs, checksums)
    print(f"line {idx+1}/1000: {line}, count {line_count}")
    total_count += line_count
print(total_count)


"""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

"""
['???', '###'] ['1', '1', '3']
['??', '??', '?##'] ['1', '1', '3']
['?#?#?#?#?#?#?#?'] ['1', '3', '1', '6']
['????', '#', '#'] ['4', '1', '1']
['????', '######', '#####'] ['1', '6', '5']
['?###????????'] ['3', '2', '1']
"""
