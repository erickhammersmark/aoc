#!/usr/bin/env python3

"""
On each line, the calibration value can be found by combining the first digit
and the last digit (in that order) to form a single two-digit number.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""

sum = 0
with open("input.txt", "r") as INPUT:
    for line in INPUT.readlines():
        digits = list(filter(lambda x: x >= "0" and x <= "9", line))
        sum += int(digits[0] + digits[-1])
print(f"Part 1: {sum}")


def build_trie(*args):
    trie = {}
    for idx, arg in enumerate(args):
        head = trie
        for letter in arg:
            head[letter] = head.get(letter, {})
            head = head[letter]
        head["value"] = str(idx)
    return trie

def try_trie(trie, letters):
    head = trie
    for letter in letters:
        if "value" in head:
            return head["value"]
        if letter not in head:
            return None
        head = head[letter]

trie = build_trie("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
for digit in range(0, 10):
    trie[str(digit)] = {"value": str(digit)}

sum = 0
with open("input.txt", "r") as INPUT:
    for line in INPUT.readlines():
        digits = []
        for idx, char in enumerate(line):
            value = try_trie(trie, line[idx:])
            if value is not None:
                digits.append(value)
        sum += int(digits[0] + digits[-1])
print(f"Part 2: {sum}")
