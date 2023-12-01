#!/usr/bin/env python3

def rps(us, them):
    """
    A rock
    B paper
    C scissors

    Wins (6 points): us B, them A; us C, them B; us A, them C
    Draws (3 points): us == them
    Losses (0 points): everything else

    We also score 1 point for choosing A, 2 for B, and 3 for C

    Return win (1), lose (-1), or draw (0) in a tuple with the score
    """

    winlose = 0
    score = ord(us) - ord("A") + 1

    if us == them:
        winlose = 0
        score += 3
    elif us == "B" and them == "A" or \
       us == "C" and them == "B" or \
       us == "A" and them == "C":
        winlose = 1
        score += 6
    else:
        winlose = -1

    print(f"Us: {us}, Them: {them}, Result: {winlose}, Score: {score}")

    return (winlose, score)


def oldscore(moves, decoder):
    _score = 0
    record = 0
    for move in moves:
        them, us = move
        ordus = ord(us) - ord("X")
        winlose, movescore = rps(decoder[ordus], them)
        _score += movescore
        record += winlose
    return (record, _score)

def score(moves, table):
    _score = 0
    record = 0
    for move in moves:
        them, outcome = move
        winlose, movescore = rps(table[outcome][them], them)
        _score += movescore
        record += winlose
    return (record, _score)

def main():
    with open("input", "r") as INPUT:
        lines = INPUT.readlines()

    moves = [tuple(l.strip().split()) for l in lines]

    decoders = [
        ["A", "B", "C"],
        ["A", "C", "B"],
        ["B", "A", "C"],
        ["B", "C", "A"],
        ["C", "A", "B"],
        ["C", "B", "A"],
    ]

    table = {
        "Z": {
            "A": "B",
            "B": "C",
            "C": "A",
        },
        "Y": {
            "A": "A",
            "B": "B",
            "C": "C",
        },
        "X": {
            "A": "C",
            "B": "A",
            "C": "B",
        },
    }

    #results = [score(moves, decoder) for decoder in decoders]
    result = score(moves, table)
    print(result)

    #print(len(moves))
    #print(results)

    #print(scores)
    #print(max(scores))


if __name__ == "__main__":
    main()



