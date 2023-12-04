#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    return parser.parse_args()

def main():
    args = parse_args()

    # Pre-compute the set of card copies won by each card
    tree = []
    for idx, line in enumerate(read_input()):
        have, need = (set(l.split()) for l in line.split(":")[1].split("|"))
        tree.append(range(idx+1, idx+1+len(have.intersection(need))))

    """
    The last card will not win any copies.

    The next to last card will win either 0 copies or 1 copy. We have already
    computed the total copies won by any copies it could win.

    The card before that could win 0 copies, a copy of the next to last one, or
    a copy of both remaining cards. Whatever the case, we have already computed
    the total copies won by each of the cards it could win.

    This works all the way up.
    """
    weights = [0] * len(tree)
    for idx in range(len(tree)-1, -1, -1):
        weights[idx] = sum(weights[child] for child in tree[idx]) + 1
    print(sum(weights))

if __name__ == "__main__":
    main()
