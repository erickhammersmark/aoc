"""
Advent of Code day 11
https://adventofcode.com/2022/day/11
"""

import sys

input_file = "input"
if len(sys.argv) > 1 and sys.argv[1] == "sample":
    input_file = "sample_input"

with open(input_file, "r") as INPUT:
    lines = [l.strip() for l in INPUT.readlines()]

"""
Part 1

Input looks like:

Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Starting items: each number is your "worry level" for that item
Operation: what happens to the worry level after the monkey inspects the item
Test: how to measure the worry level and what to do for pass/fail

After 20 rounds, which 2 monkeys have inspected the most number of items?
multiply the number of items they have inspected together.

Sample answer is 10605
"""

test_value = 1

class Monkey(object):
    """
    items: list of worry levels
    operation: function that takes one worry level and returns the post-inspection worry level
    test: function that takes the worry level and returns whether or not the test passes
    Call the instance of Monkey with a worry level and the list of monkeys
    """

    items = []
    operation = None
    test = None
    true_monkey = 0
    false_monkey = 0
    total = 0

    def __init__(self, starting_items, operation, test, true_monkey, false_monkey):
        self.items = starting_items[:]
        self.operation = operation
        self.test = test
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey

    def inspect(self, level, monkeys):
        global test_value
        self.total += 1
        level = self.operation(level) % test_value
        #level = int(level / 3)           # Part 1
        if self.test(level):
            monkeys[self.true_monkey].items.append(level)
        else:
            monkeys[self.false_monkey].items.append(level)

    def __call__(self, monkeys):
        for item in self.items:
            self.inspect(item, monkeys)
        self.items = []

    def __str__(self):
        return f"items: {self.items}"

def parse_operation(operation):
    func = f'lambda old: {operation.split("= ")[1]}'
    return eval(func)
    #return lambda old: eval(operation.split("= ")[1])

def parse_test(test):
    func = f'lambda level: level % {int(test.split("by ")[1])} == 0'
    return eval(func)
    #return lambda level: level % int(test.split("by ")[1]) == 0

monkeys = []
monkey = None
for idx, line in enumerate(lines):
    if line.startswith("Monkey"):
        starting_items = list(map(int, lines[idx+1].split(": ")[1].split(", ")))
        operation = lines[idx+2].split(": ")[1]
        test = lines[idx+3].split(": ")[1]
        test_value *= int(test.split()[-1])
        true_monkey = int(lines[idx+4].split("monkey ")[1])
        false_monkey = int(lines[idx+5].split("monkey ")[1])
        operation = parse_operation(operation)
        test = parse_test(test)
        monkeys.append(Monkey(starting_items, operation, test, true_monkey, false_monkey))

#for x in range(20):                # Part 1
for x in range(10000):              # Part 2
    print(x)
    for idx, monkey in enumerate(monkeys):
        #print(f"Monkey {idx}: {monkey}")
        monkey(monkeys)

totals = [monkey.total for monkey in monkeys]
totals.sort()
monkey_business = totals[-1] * totals[-2]
#print(f"Part 1: {monkey_business}")
print(f"Part 2: {monkey_business}")

"""
Part 2

remove the /3 and do it 10000 times instead of 20 times.
implementing by commenting out some stuff from part 1

To cope with the very large numbers, I find the product of
all of the test dividends and mod the values by them after
every operation.
"""
