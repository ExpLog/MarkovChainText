import itertools as it
from collections import Counter
import sys


def sliding_window(iter, n=3):
    """Returns a sliding window of length `n` over the iterator."""
    window = tuple(it.islice(iter, 0, n))
    if len(window) == n:
        yield window
    for element in iter:
        window = window[1:] + (element, )
        yield window


def normalize_markov(markov_chain):
    """Normalizes a markov chain."""
    total = {key: sum(map(lambda t: t[1], value)) for key, value in markov_chain.items()}
    return {key: [(word, count/total[key]) for word, count in word_list]
            for key, word_list in markov_chain.items()}


def markov_chain(file, history=3):
    """Creates a Markov Chain from a file with text, already normalized."""
    text = it.chain(*[line.split(" ") for line in file])

    history = 3
    window_counter = Counter(sliding_window(text, history+1))

    mc = {}
    for window, count in window_counter.items():
        curr_state = window[0:history]
        next_state = window[-1]
        if curr_state not in mc:
            mc[curr_state] = [(next_state, count)]
        else:
            mc[curr_state].append((next_state, count))
    return normalize_markov(mc)


file = open("test/repeating.txt", "r")
text_chain = markov_chain(file, 3)
print(text_chain)