"""
Advent of Code day 9
https://adventofcode.com/2022/day/9
"""

import math

with open("input", "r") as INPUT:
#with open("sample_input", "r") as INPUT:
    lines = [l.strip() for l in INPUT.readlines()]

"""
Part 1
Given an arbitrary grid containing a head and a tail (initially overlapping),
move the head one square at a time according to the directions and distances
laid out in the input. The tail must be in contact with the head (even diagonally),
else it must move either directly toward the had (if in the same row or col) or
diagonally toward the head.
How many squares does the tail visit?
"""

def move_in_direction(pos, direction):
    if not direction:
        return pos
    if len(direction) > 1:
        for d in direction:
            pos = move_in_direction(pos, d)
        return pos
    x, y = pos
    if direction == "U":
        pos = (x, y+1)
    elif direction == "D":
        pos = (x, y-1)
    elif direction == "L":
        pos = (x-1, y)
    elif direction == "R":
        pos = (x+1, y)
    return pos

def move_to_head(tail, head):
    tx, ty = tail
    hx, hy = head
    dist = math.sqrt((hy - ty)*(hy - ty) + (hx - tx)*(hx - tx))
    if dist < 2:
        return (tx, ty)
    move = ""
    if hx > tx:
        move = move + "R"
    elif hx < tx:
        move = move + "L"
    if hy > ty:
        move = move + "U"
    elif hy < ty:
        move = move + "D"
    return move_in_direction(tail, move)
    

head = (50, 50)
tail = (50, 50)
visited = set([tail])
for line in lines:
    direction, count = line.split()
    for _ in range(int(count)):
        head = move_in_direction(head, direction)
        tail = move_to_head(tail, head)
        visited.add(tail)
print(f"Part 1: visited {len(visited)} squares")


"""
Part 2
do the same thing, but make the series 10 long instead of 2 long.
"""

poss = [(50, 50) for s in range(10)]
visited = set([poss[-1]])
for line in lines:
    direction, count = line.split()
    for _ in range(int(count)):
        poss[0] = move_in_direction(poss[0], direction)
        for i in range(1, 10):
            poss[i] = move_to_head(poss[i], poss[i-1])
        visited.add(poss[-1])
print(f"Part 2: visited {len(visited)} squares")
