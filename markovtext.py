import sys
import itertools as it

file = open(sys.argv[1], "r")
text = it.chain([line.split(" ") for line in file])
print(text)
