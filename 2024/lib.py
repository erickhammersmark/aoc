#!/usr/bin/env python3

def read_input(filename="input.txt"):
    with open(filename, "r") as INPUT:
        return [l.rstrip("\n") for l in INPUT.readlines()]

class Board(list):
    def __init__(self, filename=None):
        if filename is not None:
            lines = read_input(filename=filename)
        else:
            lines = read_input()
        for line in lines:
            self.append(list(line))

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

