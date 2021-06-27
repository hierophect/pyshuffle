# A script for filling out the word lists in Groups Takes blocks of vocabulary
# that are organized by proximity, as words often are when imported from
# external sources, and turns the Nth column into a list of words.

# Usage: python3 grabber.py 0

# The above will allow a block of vocab test to be pasted. An empty newline will
# complete the script. The first (0th) column will be made into a list of vocab
# for a group.

import sys
output = ""
while True:
    line = input()
    if line:
        output += "," + line.split(';')[int(sys.argv[1])]
    else:
        break
print("Done.")
print(output)
