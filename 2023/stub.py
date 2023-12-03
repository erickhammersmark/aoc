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

if __name__ == "__main__":
    main()
