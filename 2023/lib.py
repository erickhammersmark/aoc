#!/usr/bin/env python3

def input():
    with open("input.txt", "r") as INPUT:
        return [l.rstrip("\n") for l in INPUT.readlines()]


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

