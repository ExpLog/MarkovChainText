import itertools as it
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
    """Checks if the word is capitalized. Expects non-empty strings"""
    return string[0].isupper()


def is_final_word(string):
    """Checks if word ends with terminal ponctuation."""
    # TODO: this sucks, change into a regexp
    return string[-1] in ".!?:;"


def discrete_sample(seq):
    """
    Samples from a discrete distribution.
    Expects a sequence where each element is a 2-tuple, of the format (element, probability).
    :param seq:
    :return:
    """
    rand = random.random()
    words, probability = zip(*seq)
    acc_words = zip(words, it.accumulate(probability))
    return next(it.dropwhile(lambda x: x[1] < rand, acc_words))[0]