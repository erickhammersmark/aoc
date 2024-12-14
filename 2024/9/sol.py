#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from lib import *

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    parser.add_argument("--two", action="store_true", default=False)
    return parser.parse_args()

args = parse_args()

line = read_input(filename=args.filename)[0]

def one():
    data = []
    fid = 0
    for idx in range(0, len(line), 2):
        data.extend([fid] * int(line[idx]))
        if idx < len(line) - 1:
            data.extend(["."] * int(line[idx+1]))
        fid += 1
    end_idx = -1
    idx = 0
    while len(data) + end_idx > idx:
        if data[idx] == ".":
            while data[end_idx] == ".":
                end_idx -= 1
            data[idx] = data[end_idx]
            data[end_idx] = "."
            end_idx -= 1
        idx += 1
    checksum = sum(idx * val for idx, val in enumerate(data) if val != ".")
    return checksum
    
def two():
    data = []
    fid = 0
    files = []
    spaces = []
    for idx in range(0, len(line), 2):
        files.append({"idx": len(data), "fid": fid, "size": int(line[idx])})
        data.extend([fid] * int(line[idx]))
        if idx < len(line) - 1:
            spaces.append({"idx": len(data), "size": int(line[idx+1])})
        if idx < len(line) - 1:
            data.extend(["."] * int(line[idx+1]))
        fid += 1
    files.reverse()
    for file in files:
        for space in spaces:
            if space["size"] >= file["size"] and space["idx"] < file["idx"]:
                for x in range(0, file["size"]):
                    data[space["idx"] + x] = data[file["idx"] + x]
                    data[file["idx"] + x] = "."
                space["size"] -= file["size"]
                space["idx"] += file["size"]
                break
    return sum(idx * val for idx, val in enumerate(data) if val != ".")

if args.two:
    print(two())
else:
    print(one())
