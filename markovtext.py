import sys
import itertools as it


def sliding_window(iter, n=3):
    """Returns a sliding window of length `n` over the iterator."""
    window = tuple(it.islice(iter, 0, n))
    if len(window) == n:
        yield window
    for element in iter:
        window = window[1:] + (element, )
        yield window


file = open(sys.argv[1], "r")
text = it.chain(*[line.split(" ") for line in file])

history = 3
for line in sliding_window(text, history):
    print(line)