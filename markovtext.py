import itertools as it
from collections import Counter
import sys
import random


def sliding_window(iter, n=3):
        """Returns a sliding window of length `n` over the iterator."""
        window = tuple(it.islice(iter, 0, n))
        if len(window) == n:
            yield window
        for element in iter:
            window = window[1:] + (element, )
            yield window


def is_capitalized(string):
    if len(string) > 0:
        return string[0].isupper()
    else:
        return False


def is_final_word(string):
    # TODO: this sucks, change into a regexp
    return string[-1] in ".!?"


def discrete_sample(seq):
    rand = random.random()
    words, probability = zip(*seq)
    acc_words = zip(words, it.accumulate(probability))
    return next(it.dropwhile(lambda x: x[1] < rand, acc_words))[0]


class MarkovChainText(object):

    def __init__(self, file, history=3):
        self.history = 3

        counter = self._window_counter(file)
        self.totals = None
        self.chain = self.normalize(self._markov_chain(counter))

        self.capital_total = sum(self.totals[key] for key in self.chain.keys() if is_capitalized(key[0]))
        self.capitals = [(key, self.totals[key]/self.capital_total)
                         for key in self.chain.keys() if is_capitalized(key[0])]

    def sample_phrases(self, n=1):
        """
        Samples a string containing `n` phrases from the learned text.
        The text will begin with a capital word and each phrase ends with one of ".?!\n"
        :return:
        """
        prev_words = discrete_sample(self.capitals)
        phrase = [word for word in prev_words]
        final_words_count = 0
        while final_words_count < n:
            try:
                next_word = discrete_sample(self.chain[prev_words])
            except:
                break
            phrase.append(next_word)
            prev_words = prev_words[1:] + (next_word,)
            if is_final_word(next_word):
                final_words_count += 1
        return phrase

    def normalize(self, mc):
        """Normalizes the markov chain and saves the totals."""
        self.totals = {key: sum(map(lambda t: t[1], value)) for key, value in mc.items()}
        return {key: [(word, count/self.totals[key]) for word, count in word_list]
                for key, word_list in mc.items()}

    def _window_counter(self, file):
        """
        Creates a Counter that counts how many times each window of
        length history+1 appears in the text.
        """
        lines = [filter(lambda x: x != "", line.rstrip("\n").split(" ")) for line in file] # the filter removes empty strings
        text = it.chain(*lines)
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


file = open("test/pg11.txt", "r")
mc_text = MarkovChainText(file)

# TODO: set random seed
print(" ".join(mc_text.sample_phrases(2)))
