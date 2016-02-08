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


class MarkovChainText(object):

    def __init__(self, file, history=3):
        self.history = 3

        counter = self._window_counter(file)
        self.totals = None
        self.chain = self._markov_chain(counter)
        self.normalize()

    def normalize(self):
        """Normalizes the markov chain and saves the totals."""
        self.totals = {key: sum(map(lambda t: t[1], value)) for key, value in self.chain.items()}
        return {key: [(word, count/self.totals[key]) for word, count in word_list]
                for key, word_list in self.chain.items()}

    def _window_counter(self, file):
        """
        Creates a Counter that counts how many times each window of
        length history+1 appears in the text.
        """
        text = it.chain(*[line.split(" ") for line in file])
        return Counter(sliding_window(text, self.history+1))

    def _markov_chain(self, window_counter):
        """Creates a Markov Chain from a file with text, already normalized."""
        mc = {}
        for window, count in window_counter.items():
            curr_state = window[0:self.history]
            next_state = window[-1]
            if curr_state not in mc:
                mc[curr_state] = [(next_state, count)]
            else:
                mc[curr_state].append((next_state, count))
        return mc


file = open(sys.argv[1], "r")
mc_text = MarkovChainText(file)

