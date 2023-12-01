"""
https://adventofcode.com/2022/day/3
"""

with open("input", "r") as INPUT:
    lines = INPUT.readlines()

def priority(item):
    if ord(item) >= ord("a") and ord(item) <= ord("z"):
        return ord(item) - ord("a") + 1
    return ord(item) - ord("A") + 27

# part 1
#total = 0
#for line in (l.strip() for l in lines):
#    half = int(len(line)/2)
#    first = line[:half]
#    second = line[half:]
#    for c in first:
#        if c in second:
#            total += priority(c)   
#            #print(first, second, c, priority(c))
#            break
#print(total)

lines = [l.strip() for l in lines]
if len(lines) % 3 != 0:
    raise Exception(f"Input has {len(lines)} lines, which is not devisible by 3")

groups = [lines[i*3:i*3+3] for i in range(0, int(len(lines)/3))]

total = 0
for group in groups:
    for item in group[0]:
        if item not in group[1] or item not in group[2]:
            continue
        total += priority(item)
        break
print(total)
