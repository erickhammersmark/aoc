"""
Advent of Code day 6
https://adventofcode.com/2022/day/6
"""

with open("input", "r") as INPUT:
    line = INPUT.read()

packet_marker_len = 4
message_marker_len = 14

# Part 1
#marker = packet_marker_len

# Part 2
marker = message_marker_len

for idx in range(len(line)):
    if len(set(line[idx-marker:idx])) == marker:
        print(idx)
        break
