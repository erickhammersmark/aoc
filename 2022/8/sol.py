"""
Advent of Code day 8
https://adventofcode.com/2022/day/8
"""

with open("input", "r") as INPUT:
    lines = [list(l.strip()) for l in INPUT.readlines()]

#lines = [
#    "30373",
#    "25512",
#    "65332",
#    "33549",
#    "35390",
#]
#lines = [list(l) for l in lines]

"""
Part 1
How many trees are visible from outside the grid?
The answer for the sample data is 21: the 16 edges plus the 5
interior trees that are not blocked by a large tree in at least
one direction all the way to the edge of the grid.
"""

def visible_left(line, row):
    """
    Return the list of indices visible from the left.
    """
    visible = [(row, 0)]
    height = line[0]
    for idx, tree in enumerate(line[1:]):
        idx += 1
        if tree > height:
            height = tree
            visible.append((row, idx))
    return visible


def visible_left_right(line, row):
    left = visible_left(line, row)
    line.reverse()
    right = [(row, len(line) - idx[1] - 1) for idx in visible_left(line, row)]
    line.reverse()
    visible = set(left)
    visible.update(set(right))
    #print(f"line {line}, visible {visible}")
    return visible

visible = set()
for idx, line in enumerate(lines):
    visible.update(visible_left_right(line, idx))

transposed = [[line[x] for line in lines] for x in range(len(lines[0]))]

for idx, line in enumerate(transposed):
    transposed_visible = visible_left_right(line, idx)
    visible.update(set((y, x) for x, y in transposed_visible))

print(f"Total visible trees (part 1): {len(visible)}")


"""
Part 2
Which tree has the best view of other trees?
count the number of trees in each direction until you reach
a tree of that height or higher, multiply the 4 results together,
that's the tree's score.
"""

highest_score = 0

for c in range(len(lines[0])):
    for r in range(len(lines)):
        tree = lines[r][c]

        up = 0
        for y in range(r-1, -1, -1):
            up += 1
            if lines[y][c] >= tree:
                break

        down = 0
        for y in range(r+1, len(lines)):
            down += 1
            if lines[y][c] >= tree:
                break

        left = 0
        for x in range(c-1, -1, -1):
            left += 1
            if lines[r][x] >= tree:
                break

        right = 0
        for x in range(c+1, len(lines[0])):
            right += 1
            if lines[r][x] >= tree:
                break
        
        highest_score = max(highest_score, up * down * left * right)

print(f"Part 2 highest scenic score: {highest_score}")
