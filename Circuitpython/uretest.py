import re
import sys

regex = sys.argv[1]
istring = sys.argv[2]
outlist = []

match = re.search(regex,istring)

while (match):
    print(match)
    print(match.group(0))
    print(match.group(1))

    outlist.append(match.group(1))
    print(match.end())
    istring = istring[match.end():]
    print(istring)
    match = re.search(regex,istring)

print(outlist)
print("EXIT")
