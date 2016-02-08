import itertools as it
from collections import Counter

from markov.utils import sliding_window, is_capitalized, is_final_word, discrete_sample


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
        return " ".join(phrase)

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
        return Counter(sliding_window(text, self.history + 1))

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


#file = open("test/pg11.txt", "r")
#mc_text = MarkovChainText(file, 2)

#print(mc_text.sample_phrases())
