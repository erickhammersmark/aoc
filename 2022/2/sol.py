#!/usr/bin/env python3

class Elf(object):
    rations = []
    calories = 0

with open("input", "r") as INPUT:
    lines = INPUT.readlines()

elves = [Elf()]
for line in (l.strip() for l in lines):
    if line:
        elves[-1].rations.append(int(line))
        elves[-1].calories += int(line)
    else:
        elves.append(Elf())

elves.sort(key=lambda x: int(x.calories))
top3 = elves[-3:]
print(top3)
print([elf.calories for elf in top3])
print(sum(elf.calories for elf in top3))
