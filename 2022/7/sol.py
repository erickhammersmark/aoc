"""
Advent of Code day 7
https://adventofcode.com/2022/day/7
"""

with open("input", "r") as INPUT:
    lines = [l.strip() for l in INPUT.readlines()]

total_size = 0
stack = [0]
sums = []
part1sum = 0
for line in lines:
    if line == "$ cd ..":
        thisdir = stack.pop()
        sums.append(thisdir)
        if thisdir < 100000:
            part1sum += thisdir
        stack[-1] += thisdir
        continue
    if line.startswith("$ cd"):
        stack.append(0)
        continue
    if line == "$ ls":
        continue
    if line.startswith("dir"):
        continue
    filesize = int(line.split()[0])
    total_size += filesize
    stack[-1] += filesize

while len(stack) > 1:
    thisdir = stack.pop()
    sums.append(thisdir)
    if thisdir < 100000:
        part1sum += thisdir
    stack[-1] += thisdir

print(f"Part 1 sum: {part1sum}")

sums.sort()

free = 70 * 1000 * 1000 - total_size
needed = 30 * 1000 * 1000 - free
print(f"Part 2 free: {free}, needed: {needed}, size: ", end="")
for size in sums:
    if size > needed:
        print(size)
        break
