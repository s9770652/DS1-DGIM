"""Estimates the occurrences of mushroom odours, separated by edibility."""

__author__ = "Zeno Adrian Weil"

from dgim import Dgim

ODOURS = {
    'a': 0, 'l': 1, 'c': 2, 'y': 3, 'f': 4, 'm': 5, 'n': 6, 'p': 7, 's': 8
}


def read_data():
    """Reads-in mushroom data and one-hot encodes the odour."""
    codes = {k: [True if i == v else False for i in range(9)] for k, v in ODOURS.items()}
    with open('agaricus-lepiota.data', mode='r') as file:
        lines = file.readlines()
        edible, poisonous = [], []
        for line in lines:
            if line[0] == 'e':
                edible.append(codes[line[2*5]])  # Odour is the sixth attribute.
            else:
                poisonous.append(codes[line[2*5]])
    return edible, poisonous

def isolate_column(data, odour):
    """Returns a binary list including one codepoint only."""
    return [code[ODOURS[odour]] for code in data]

def real_count(data, N):
    """Counts odour occurrences in the last N mushrooms."""
    return sum(data[-N:])

def dgim_count(data, N, error_rate):
    """Estimates odour occurrences in the last N mushrooms."""
    dgim = Dgim(N, error_rate)
    for i in range(len(data)):
        dgim.update(data[i])
    return dgim.get_count()
