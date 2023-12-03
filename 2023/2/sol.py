#!/usr/bin/env python

import sys
sys.path.append("..")

from argparse import ArgumentParser
from collections import defaultdict
from lib import read_input

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--filename", default="input.txt")
    return parser.parse_args()

def main():
    args = parse_args()

    limits = { "red": 12, "green": 13, "blue": 14 }
    game_sum = 0
    power_sum = 0
    
    for line in read_input(filename=args.filename):
        atleast = {"red": 0, "green": 0, "blue": 0}
        game, blocks = line.split(":")
        game_no = int(game.split()[1])

        draws = blocks.split(";")
        for draw in draws:
            blockcounts = draw.split(",")
            for blockcount in blockcounts:
                count, color = blockcount.split()
                count = int(count)
                if count > atleast[color]:
                    atleast[color] = count
                if count > limits[color]:
                    #print(f"Game {game_no} impossible as {color} count of {count} exceeds limit of {limits[color]}")
                    game_no = 0
        game_sum += game_no
        power_sum += atleast["red"] * atleast["green"] * atleast["blue"]
    print(f"Part 1, sum of possible games given limits {limits}: {game_sum}")
    print(f"Part 2, sum acorss all games of the product of the least possible counts for all colors: {power_sum}")

if __name__ == "__main__":
    main()

"""
['Game', '1:', '5', 'red,', '1', 'green,', '2', 'blue;', '2', 'green,', '8', 'blue,', '6', 'red;', '8', 'red,', '3', 'blue,', '2', 'green;', '6', 'red,', '1', 'green,', '19', 'blue;', '1', 'red,', '17', 'blue']
['Game', '2:', '4', 'red,', '5', 'green,', '2', 'blue;', '7', 'red,', '14', 'green,', '3', 'blue;', '2', 'green,', '5', 'blue,', '11', 'red;', '10', 'blue,', '3', 'green;', '9', 'green,', '6', 'blue,', '13', 'red;', '7', 'red,', '5', 'green,', '9', 'blue']
['Game', '3:', '9', 'green,', '18', 'blue,', '1', 'red;', '6', 'red,', '10', 'blue,', '5', 'green;', '4', 'blue,', '4', 'red,', '15', 'green']
['Game', '4:', '1', 'red,', '13', 'green;', '10', 'green,', '2', 'red;', '3', 'red,', '4', 'green,', '2', 'blue']
['Game', '5:', '4', 'red,', '2', 'green,', '1', 'blue;', '4', 'red,', '9', 'blue;', '4', 'green,', '1', 'red,', '6', 'blue;', '3', 'blue,', '2', 'green,', '6', 'red;', '5', 'red,', '4', 'green,', '1', 'blue']
"""
