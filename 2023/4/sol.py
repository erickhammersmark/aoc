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

    result = 0
    for line in read_input():
        have, need = ( set(nums.split()) for nums in line.split(":")[1].split("|") )
        result += int(pow(2, len( have.intersection(need) ) - 1))

    print(result)


if __name__ == "__main__":
    main()
