#!/usr/bin/env python3

with open("input", "r") as INPUT:
    lines = INPUT.readlines()

rations = [[]]
calories = [0]
max_calories = 0
max_i = 0
for line in (l.strip() for l in lines):
    if line:
        rations[-1].append(int(line))
        calories[-1] += int(line)
        if calories[-1] > max_calories:
            max_calories = calories[-1]
            max_i = len(calories) - 1
    else:
        rations.append([])
        calories.append(0)

print(calories)
print(max_calories, max_i)
