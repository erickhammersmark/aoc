#!/usr/bin/env python3

def read_input(filename="input.txt"):
    with open(filename, "r") as INPUT:
        return [l.rstrip("\n") for l in INPUT.readlines()]

class Board(list):
    ROW=0
    COL=1
    R=ROW
    C=COL
    X=COL
    Y=ROW
 
    def __init__(self, *args, filename=None, try_type=None, example=False):
        if args:
            lines = args[0]
        elif example:
            lines = read_input(filename="example.txt")
        elif filename is not None:
            lines = read_input(filename=filename)
        else:
            lines = read_input()
        for line in lines:
            line = list(line)
            if try_type is not None:
                for idx, val in enumerate(line):
                    try:
                        line[idx] = try_type(val)
                    except:
                        pass
            self.append(line)

    def find(self, target, findall=False):
        results = []
        for idx, row in enumerate(self):
            for col, val in enumerate(row):
                if val == target:
                    if not findall:
                        return (idx, col)
                    results.append(idx, col)
        return results

    def print(self):
        for row in self:
            print("".join(map(str,row)))

    def get(self, pos, default=None):
        if self.oob(pos):
            return default
        try:
            return self[pos[0]][pos[1]]
        except Exception as e:
            return default

    def set(self, pos, val):
        if not pos or len(pos) != 2:
            return False
        if self.oob(pos):
            return False
        self[pos[0]][pos[1]] = val

    def neighbors(self, pos, diagonal=False, include_oob=False):
        neighbors = []
        R_up = pos[self.R] - 1
        R_down = pos[self.R] + 1
        C_left = pos[self.C] - 1
        C_right = pos[self.C] + 1

        if diagonal:
            neighbors.append((R_up, C_left))
            neighbors.append((R_up, C_right))
            neighbors.append((R_down, C_right))
            neighbors.append((R_down, C_left))

        neighbors.append((R_up, pos[self.C]))
        neighbors.append((R_down, pos[self.C]))
        neighbors.append((pos[self.R], C_left))
        neighbors.append((pos[self.R], C_right))

        def tooobornottooob(neighbor):
            if include_oob:
                return True
            if self.oob(neighbor):
                return False
            return True

        return list(
            filter(
                tooobornottooob, neighbors
            )
        )

    def copy(self):
        """
        Return a copy of the board, including unique copies of each row.
        Does not create unique copies of the values.
        """
        board_copy = self[:]
        for idx in range(0, len(self)):
            board_copy[idx] = board_copy[idx][:]

    def oob(self, pos):
        if len(self) == 0:
            return True
        if pos[0] < 0 or pos[1] < 0:
            return True
        if pos[0] >= len(self) or pos[1] >= len(self[0]):
            return True
        return False

    dir_to_english = {
        (1, 0): "down",
        (-1, 0): "up",
        (0, 1): "right",
        (0, -1): "left",
    }

    def direction(self, _from, _to, english=False):
        """
        up, down, left, right only.
        """
        if _from[0] != _to[0] and _from[1] != _to[1]:
            return None
        if _from == _to:
            return None
        
        _dir = tuple(1 if t > f else -1 if f > t else 0 for t, f in zip(_to, _from))
        if english:
            return self.dir_to_english[_dir]
        return _dir

    def points_between(self, _from, _to):
        """
        Only supports pairs along a straight line.
        Includes _to, does not include _from.
        """
        if _from[0] != _to[0] and _from[1] != _to[1]:
            return []
        if _from == _to:
            return []
        DIR = 0
        if _from[DIR] == _to[DIR]:
            DIR = 1
        delta = 1 if _to[DIR] > _from[DIR] else -1 if _from[DIR] > _to[DIR] else 0
        point = list(_from)
        points = []
        while point[DIR] != _to[DIR]:
            point[DIR] += delta
            points.append(tuple(point))
        return points

    def pos_difference(self, _from, _to):
        return (_to[0] - _from[0], _to[1] - _from[1])

    def invert_pos(self, pos):
        return (0 - pos[0], 0 - pos[1])

    def add_pos(self, a, b):
        return (a[0] + b[0], a[1] + b[1])

def build_trie(*args, values=None):
    trie = {}
    for idx, arg in enumerate(args):
        head = trie
        for letter in arg:
            head[letter] = head.get(letter, {})
            head = head[letter]
        if values is not None:
            head["value"] = values[idx]
        else:
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

