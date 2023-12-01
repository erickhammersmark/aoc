"""
Advent of Code day 12
https://adventofcode.com/2022/day/12
"""

import sys

calls = 0

input_file = "input"
if len(sys.argv) > 1 and sys.argv[1] == "sample":
    input_file = "sample_input"

with open(input_file, "r") as INPUT:
    lines = [l.strip() for l in INPUT.readlines()]


"""
Part 1

Given a landscape like:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Find the length of the shortest path from S to E that moves
only up, down, left, or right and never increases by more than
one letter (but can do down as many letters as you want).

Sample's answer is 31
"""

def height(pos):
    row, col = pos
    letter = lines[row][col]
    if letter == "S":
        return ord("a")
    if letter == "E":
        return ord("z")
    return ord(letter)

def inbounds(point):
    """
    point is (row, col)
    """
    if point[0] < 0 or point[0] >= len(lines):
        return False
    if point[1] < 0 or point[1] >= len(lines[0]):
        return False
    return True

def isvalid(point, path):
    if point in path:
        return False
    if height(point) - height(path[-1]) > 1:
        return False
    return True

board = []
S = None
E = None
for idx, line in enumerate(lines):
    board.append(list(line))
    if "S" in line:
        S = (idx, line.index("S"))
    if "E" in line:
        E = (idx, line.index("E"))

class Heightmap(object):
    max_dist = 99999999
    def __init__(self, board, S, E):
        self.board = board
        self.cur = S
        self.E = E
        self.unvisited = set()
        self.distances = dict()
        self.paths = [[S]]
        self.uphill = True
        for row_idx, row in enumerate(self.board):
            for col_idx, letter in enumerate(row):
                self.unvisited.add((row_idx, col_idx))
                self.distances[(row_idx, col_idx)] = self.max_dist
        self.distances[self.cur] = 0

    def height(self, point):
        row, col = point
        letter = self.board[row][col]
        if letter == "S":
            return ord("a")
        if letter == "E":
            return ord("z")
        return ord(letter)

    def inbounds(self, point):
        if point[0] < 0 or point[0] >= len(self.board):
            return False
        if point[1] < 0 or point[1] >= len(self.board[0]):
            return False
        return True

    def isvalid(self, point):
        if self.uphill and self.height(point) - self.height(self.cur) > 1:
            return False
        if (not self.uphill) and self.height(self.cur) - self.height(point) > 1:
            return False
        return True

    def neighbors(self):
        neighbors = []
        for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbors.append((self.cur[0] + direction[0], self.cur[1] + direction[1]))
        return neighbors

    def findE(self):
        while self.E in self.unvisited:
            for neighbor in self.neighbors():
                if neighbor not in self.unvisited:
                    continue
                if not self.isvalid(neighbor):
                    continue
                if self.distances[neighbor] > self.distances[self.cur] + 1:
                    self.distances[neighbor] = self.distances[self.cur] + 1
            self.unvisited.remove(self.cur)
            smallest_unvisited_distance = self.max_dist
            for node in self.unvisited:
                if self.distances[node] < smallest_unvisited_distance:
                    self.cur = node
                    smallest_unvisited_distance = self.distances[node]
            if self.cur not in self.unvisited:
                break
        return self.distances[self.E]

hm = Heightmap(board, S, E)

print(f"Part 1: {hm.findE()}")

"""
Part 2
Instead, find the shortest path from E down to any location of height a.
Maintain the adjacency requirement (i.e. this will be a hiking path from
somewhere of height a to position E, adjacent positions cannot increase
in height by more than one.
"""

a_locs = []
for row_idx, row in enumerate(board):
    for col_idx, letter in enumerate(row):
        if letter == "a" or letter == "S":
            a_locs.append((row_idx, col_idx))

num_as = len(a_locs)
distances = []
for idx, a_loc in enumerate(a_locs):
    print(f"{idx + 1}/{num_as}")
    hm = Heightmap(board, E, a_loc)
    hm.uphill = False
    distances.append(hm.findE())

print(f"Part 2: {min(distances)}")



"""
Brute force, fine for the sample, not for the input

def findE(pos, Epos, path=[]):
    global calls
    calls += 1
    print(calls)
    #print(f"findE({pos}, {Epos}, {path})")
    path = path[:]
    path.append(pos)
    if pos == Epos:
        return len(path)
    results = []
    for r in [-1, 1]:
        _p = (pos[0]+r, pos[1])
        if inbounds(_p) and isvalid(_p, path):
            results.append(findE(_p, Epos, path))
        #else:
        #    print(f"rejected {_p}: inbounds: {inbounds(_p)}, isvalid: {inbounds(_p) and isvalid(_p, path)}")
    for c in [-1, 1]:
        _p = (pos[0], pos[1]+c)
        if inbounds(_p) and isvalid(_p, path):
            results.append(findE(_p, Epos, path))
        #else:
        #    print(f"rejected {_p}: inbounds: {inbounds(_p)}, isvalid: {inbounds(_p) and isvalid(_p, path)}")
    #print(f"results: {results}")
    if not results:
        return 0
    if all([r == 0 for r in results]):
        return 0
    return min([r for r in results if r != 0])

pathlen = findE(S, E)
print(f"Part 1: {pathlen - 1}")
"""
