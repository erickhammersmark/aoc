"""
Advent of Code day X
https://adventofcode.com/2022/day/X
"""

with open("input", "r") as INPUT:
    lines = (l.strip() for l in INPUT.readlines())

"""
Part 1

Given a board like:
[A]     [B]
[C] [D] [E]
 1   2   3

And a set of moves like:

move 2 from 3 to 2

Produce the set of topmost letters after making all of the moves
"""

moves = []
board = []
for line in lines:
    if not line:
        continue
    if "move" in line:
        mv, count, frm, source, t, dest = line.split()
        moves.append(tuple(map(int, (count, source, dest))))
    else:
        board.append(line)

num_cols = int(board[-1].split()[-1])
board.pop(-1)

brd = [[] for x in range(0, num_cols + 1)]
for line in board:
    count = 1
    for col in range(1, num_cols * 4, 4):
        if col < len(line) and line[col] != " ":
            brd[count].append(line[col])
        count += 1

"""
brd is now a 2d array where the outer dimension is stacks (indexed as in the moves)
and the inner dimension is each stack, element 0 == top of stack. pop(0) to pull one
off of the top, insert(0,) to push one onto the top.
"""

for count, source, dest in moves:
    for _ in range(count):
        brd[dest].insert(0, brd[source].pop(0))

result = [stack[0] for stack in brd if stack]
print("".join(result))

"""
Part 2

Preserve the order of crates during each move
"""

brd = [[] for x in range(0, num_cols + 1)]
for line in board:
    count = 1
    for col in range(1, num_cols * 4, 4):
        if col < len(line) and line[col] != " ":
            brd[count].append(line[col])
        count += 1

for count, source, dest in moves:
    brd[dest] = brd[source][0:count] + brd[dest]
    brd[source] = brd[source][count:]

result = [stack[0] for stack in brd if stack]
print("".join(result))
