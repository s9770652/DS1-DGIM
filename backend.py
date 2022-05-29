"""Estimates the significance of mushroom characteristics for edibility."""

__author__ = 'Zeno Weil'

from random import shuffle
from dgim import Dgim

ODORS = {
    'a': 0, 'l': 1, 'c': 2, 'y': 3, 'f': 4, 'm': 5, 'n': 6, 'p': 7, 's': 8
}


def read_data():
    """Reads-in mushroom data and one-hot encodes the odor."""
    codes = {k: [True if i == v else False for i in range(9)] for k, v in ODORS.items()}
    with open('agaricus-lepiota.data', mode='r') as file:
        lines = file.readlines()
        edible, poisonous = [], []
        for line in lines:
            if line[0] == 'e':
                edible.append(codes[line[2*5]])  # Odor is the sixth attribute.
            else:
                poisonous.append(codes[line[2*5]])
    shuffle(edible)
    shuffle(poisonous)
    return edible, poisonous


def isolate_odor(data, odor):
    """Returns a list including one encoding only."""
    return [code[ODORS[odor]] for code in data]


def true_count(data, N):
    return sum(data[-N:])


def dgim_count(data, N, error_rate=0.5):
    dgim = Dgim(N, error_rate)
    for i in range(len(data)):
        dgim.update(data[i])
    return dgim.get_count()


if __name__ == '__main__':
    edible, poisonous = read_data()
    edible = isolate_odor(edible, 'n')
    poisonous = isolate_odor(poisonous, 'n')
    N = 2048
    print("true e", true_count(edible, N))
    print("dgim e", dgim_count(edible, N))
    print("true p", true_count(poisonous, N))
    print("dgim p", dgim_count(poisonous, N))
