#!python3
"""Solves combinatorial 'if you can't move you lose' word games."""
import string
from collections import defaultdict

def mex(s):
    i = 0
    while i in s:
        i += 1
    return i

def solve(moves_from, positions=None):
    """Solve word game dictionary of moves from each position."""
    if positions == None:
        positions = list(moves_from.keys())
    else:
        positions = list(positions)

    nimbers = dict()

    for word in positions:
        nimbers[word] = mex(nimbers[move] for move in moves_from[word])

    print("Pruning strategy...")
    strategy = dict()
    for word in positions:
        if not moves_from[word]:
            strategy[word] = []
            continue

        if nimbers[word] == 0:
            # player moving has lost. might move anywhere to be difficult
            children = [strategy[move] for move in moves_from[word]]
            strat = list()
            for child in children:
                strat.extend(child)
            strat = sorted(strat, key=lambda x: (len(x), x))
        else:
            # move to a zero
            children = [[move] + strategy[move] for move in moves_from[word] if nimbers[move] == 0]
            assert children
            # choose shortest to remember
            strat = min(children, key=len)

        strategy[word] = strat

    return nimbers, strategy

print ("Loading dictionary...")
words = list()
for line in open("yawl.txt"):
    word = line.strip()
    if set(word).issubset(string.ascii_lowercase) and len(word) > 1:
        words.append(word)

for vowel in "aeiou":
    words.append(vowel)

def add_and_rearrange():
    positions = words+[""]
    positions.sort(key=len, reverse=True)

    moves_from_crib = defaultdict(set)
    def crib_for(word):
        return "".join(sorted(word))

    for word in words:
        crib = crib_for(word)
        for i in range(0, len(crib)):
            old = crib[0:i] + crib[i+1:]
            moves_from_crib[old].add(word)

    moves_from = dict()
    for word in positions:
        moves_from[word] = moves_from_crib[crib_for(word)]

    return moves_from, positions

if __name__ == "__main__":
    print("Building game tree for 'add a letter and rearrange'...")
    moves_from, positions = add_and_rearrange()
    print("Solving game...")
    nimbers, strategy = solve(moves_from, positions)
    winner = "first" if nimbers[""] else "second"
    print("In the 'add a letter and rearrange' game")
    print("The {0} player can always win.".format(winner))
    print("A winning strategy for them is")
    winning_strategy = strategy[""]
    print(winning_strategy)
    print("That's {0} words to remember!".format(len(winning_strategy)))
