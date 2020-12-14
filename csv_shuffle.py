import random
import csv
import json
import re
import inquirer
import sys
import itertools

inq_theme = inquirer.themes.Default()
if len(sys.argv) > 1:
    if sys.argv[1] == "green":
        inq_theme = inquirer.themes.GreenPassion()


# Deck Sections are selectables, Categories, Pair Groups and Cards.
# Deck Categories are selectable types like Pronouns or nouns, and card
# groupings based on study topic (like lingodeer chapters).

# Parse deck file into dictionary
d_data = {}
d_section = "invalid group"
d_category = "invalid subgroup"
d_catagory_readkeys = False
selectable_keys = []

group_keys = ["name","word-type","key-type","key-list"]

with open('deck.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    # Increment through the rows in the file, changing list levels as required
    for row in csv_reader:
        print(row)
        if (not row) or (row[0][:2] == "//"):
            continue
        # Change section
        if row[0][:2] == "# ":
            name = row[0][2:]
            d_data[name] = dict()
            d_section = name
            continue
        # Change category within a section, mark to read keys next row
        if row[0][:3] == "## ":
            name = row[0][3:]
            d_data[d_section][name] = list()
            d_category = name
            d_catagory_readkeys = True
            continue
        # Read category keys after a category header
        if d_catagory_readkeys:
            selectable_keys = row
            d_catagory_readkeys = False
            continue
        # Otherwise set items
        if d_section == "Selectables":
            #for each item in the row, make a dict entry based on selectable keys
            d_data[d_section][d_category].append({selectable_keys[i]:row[i] for i in range(len(row))})
        elif d_section == "Groups":
            #create dict entries, then replace lists entries with lists
            d_data[d_section][row[0]] = {group_keys[i]:row[i] for i in range(1,len(row))}
            parsedlist = d_data[d_section][row[0]]["key-list"][1:-1].split(",")
            d_data[d_section][row[0]]["key-list"] = parsedlist
            print(d_data[d_section][row[0]])
        elif d_section == "Cards":
            d_card = {}
            d_card["side_names"] = selectable_keys
            d_card["sides"] = row
            d_data[d_section][d_category].append(d_card)
            # keylist = re.findall(r"\[(.*?)\]", row[0])
            # index = len(d_data[d_section][d_category])-1
            # d_data[d_section][d_category][index]["key-list"] = keylist

print(d_data)
print(json.dumps(d_data,indent=4))

# ----------
# Helper fucntions
# ----------

def get_card_permutations(card, requested):
    keylist = card["key-list"]
    #print(keylist)
    maximums = [len(d_data["Categories"][item]["key-list"]) for item in keylist]
    #print(maximums)
    ranges = [range(0,m) for m in maximums]
    #print(ranges)
    outlist = list(itertools.product(*ranges))
    #print(outlist)
    random.shuffle(outlist)
    #print(outlist)
    #print(outlist[:requested])
    return outlist[:requested]

def card_permutation_to_string(cards, index, side, perms):
    #print(cards[index][side])
    frags = cards[index][side].split("[")
    outlist = ""
    perm_idx = 0;
    for frag in frags:
        #print(frag)
        if frag.find("]") != -1:
            frag = frag[frag.find("]")+1:]
            #print(frag)
            key = cards[index]["key-list"][perm_idx]
            #print(key)
            selectable = d_data["Categories"][key]["word_type"]
            keytype = d_data["Categories"][key]["key_type"]
            #print(selectable)
            insert = d_data["selectables"][selectable][perms[perm_idx]][keytype]
            #print(insert)
            outlist = outlist + insert + frag
            perm_idx += 1
        else:
            outlist = outlist + frag
    #print(outlist)
    return outlist

# ------------------------------------
# Command line interface for Mac/Linux
# ------------------------------------

print("PyShuffle 0.0.1 (Nov 2020)")
print("Pulling cards from 'deck.csv'")
# using inquirer
questions = [
  inquirer.Checkbox('cards',
                message="Select study groups with Spacebar. Press enter to begin",
                choices=d_data["Cards"]
            ),
]
study_group = []
while not study_group:
    answers = inquirer.prompt(questions, theme=inq_theme)
    study_group = answers["cards"]
    if not study_group:
        print("You must select at least one group")

# Study group is the list of card subgroups (like textbook chapters)
print("study_group")
print(study_group)

## Combine all cards in study group list into a single list
sublists = [d_data["Cards"][s] for s in study_group]
scards = [item for sublist in sublists for item in sublist]
sorder = []

# for card in scards
    # Generate (rep #) of card variation tuples
    # for side in cards
        # generate side mapping index list
        # generate variation string tuple
        # for tuple in variation tuples
            # iterate through side string
            # replace each replacable with a selectable

# TODO: move key type out of data structure and calculate it on the fly

CARD_REPS = 5 # max number of repeats of a card

# for every card
for i in range(len(scards)):
    # get a list of all keys on the card's first side
    print("Scards 0:")
    print(scards[0])
    breakpoint()
    keylist = re.findall(r"\[(.*?)\]", scards[0])
    perms = get_card_permutations(scards[i], CARD_REPS)
    print(perms)
    #for side in scards[i]:



# for i in range(len(scards)):
#     #print("--------Loop:" + str(i))
#     #print(scards[i])
#     iterations = get_card_permutations(scards[i],5)
#     #print("iterations")
#     #print(iterations)
#     for side in scards[i]:
#         if side == "key-list":
#             continue
#         if iterations:
#             for t in iterations:
#                 sorder.append((i, side, t))
#         else:
#             sorder.append((i, side, False))
# #print("unshuffled")
# #print(sorder)
# random.shuffle(sorder)
# #print("shuffled")
# #print(sorder)

# for i in range(len(sorder)):
#     first = card_permutation_to_string(scards, sorder[i][0], sorder[i][1], sorder[i][2])
#     print(first)
#     input()
#     for side in scards[sorder[i][0]]:
#         if side == "key-list":
#             continue
#         print(card_permutation_to_string(scards,sorder[i][0],side,sorder[i][2]))

# print("end")

