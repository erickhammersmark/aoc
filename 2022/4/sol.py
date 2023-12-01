"""
Advent of Code day 4
https://adventofcode.com/2022/day/4
"""

with open("input", "r") as INPUT:
    lines = [l.strip() for l in INPUT.readlines()]


"""
Part 1
input contains comma-separated pairs of ranges, such as 2-4,6-8.
find the count of pairs where one range is a proper subset of the other.
"""

def line_to_sets(line):
    a, b = line.split(",")

    a1, a2 = a.split("-")
    asgt_a = set(range(int(a1), int(a2)+1))

    b1, b2 = b.split("-")
    asgt_b = set(range(int(b1), int(b2)+1))

    return [asgt_a, asgt_b]

count = 0
for line in lines:
    a, b = line_to_sets(line)
    if a.issubset(b) or b.issubset(a):
        count += 1
print(f"Number of propper subsets in pairs: {count}")


"""
Part 2
find the number of pairs that overlap at all
"""

count = 0
for line in lines:
    a, b = line_to_sets(line)
    if a.intersection(b):
        count += 1
print(f"Number of intserecting pairs: {count}")
