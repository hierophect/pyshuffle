import random
import csv
import json
import re
import inquirer
import sys
import itertools

DEBUG = False

def log(pre, s):
    if DEBUG:
        print(pre + ": "+ str(s))

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

log("data", json.dumps(d_data,indent=4,ensure_ascii=False))

# ----------
# Helper fucntions
# ----------

def get_key_permutations(keylist, requested):
    maximums = [len(d_data["Groups"][item]["key-list"]) for item in keylist]
    ranges = [range(0,m) for m in maximums]
    outlist = list(itertools.product(*ranges))
    random.shuffle(outlist)
    return outlist[:requested]

def card_permutation_to_string(cards, index, side, perms):
    #print(cards[index][side])
    frags = cards[index][side].split("[")
    outstring = ""
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
            outstring = outstring + insert + frag
            perm_idx += 1
        else:
            outstring = outstring + frag
    #print(outstring)
    return outstring

# ------------------------------------
# Command line interface for Mac/Linux
# ------------------------------------

print("PyShuffle 0.0.1 (Nov 2020)")
print("Pulling cards from 'deck.csv'")
# using inquirer
# questions = [
#   inquirer.Checkbox('cards',
#                 message="Select study groups with Spacebar. Press enter to begin",
#                 choices=d_data["Cards"]
#             ),
# ]
# study_group = []
# while not study_group:
#     answers = inquirer.prompt(questions, theme=inq_theme)
#     study_group = answers["cards"]
#     if not study_group:
#         print("You must select at least one group")

#DEBUG: don't want to select groups every time I run it
study_group = d_data["Cards"].keys()

# Study group is the list of card subgroups (like textbook chapters)
log("study_group", study_group)

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
# (wait, why tho?)

CARD_REPS = 5 # max number of repeats of a card

log("scards", scards)
# for every card
for i in range(len(scards)):
    # get a list of all keys on the card's first side
    keylist = re.findall(r"\[(.*?)\]", scards[i]["sides"][0])
    # Get a list of permutation tuples
    perms = get_key_permutations(keylist, CARD_REPS)
    log("perms", perms)

    #TODO: Should probably do permutations/sides here, instead
    # because I do sides/permutations I can't add to sorder directly.
    sorder_batch = []
    for j in range(len(perms)):
        sorder_batch.append({})

    for idx, side in enumerate(scards[i]["sides"]):
        log("side", side)
        side_name = scards[i]["side_names"][idx]
        # TODO: obtain variation tuples
        # this step will also sanitize the keylist between sides for index comparison
        # for now, fake by using default of side names
        variations = [side_name] * len(keylist)
        log("variations",variations)
        #breakpoint()

        # map to the first keylist, assuming (for now) that all
        # groups are unique
        side_idx_map = []
        #todo: this needs to only take material before the ":" used in compound replacables
        new_keylist = re.findall(r"\[(.*?)\]", side)
        for key in new_keylist:
            for j in range(len(keylist)):
                if keylist[j] == key:
                    side_idx_map.append(j)
                    break
        log("side idx",side_idx_map)

        # create a side instance for every permutation
        for p_idx, perm in enumerate(perms):
            frags = side.split("[")
            log("frags", frags)
            outstring = frags[0]

            for f_idx, frag in enumerate(frags[1:]):
                log("frag",frag)
                # every frag but the first should start with a keystring
                frag = frag[frag.find("]")+1:]
                log("frag cut:", frag)

                key = keylist[side_idx_map[f_idx]]
                log("key", key)

                group = d_data["Groups"][key]
                key_sel = d_data["Groups"][key]["key-list"][perm[f_idx]]
                log("key_sel", key_sel)
                log("group_sel", group)
                sel = ""
                log("variant", variations[f_idx])

                log("selectables", d_data["Selectables"][group["word-type"]])

                for selectable in d_data["Selectables"][group["word-type"]]:
                    if (selectable[group["key-type"]] == key_sel):
                        sel = selectable[variations[f_idx]]
                log("sel", sel)
                outstring = outstring + sel + frag
                log("outstring", outstring)

            print(outstring)
            print(p_idx)
            #sorder_batch[p_idx] = {}
            sorder_batch[p_idx][side_name] = outstring
            #sorder_batch[p_idx].update({side_name:outstring})
            print(json.dumps(sorder_batch,indent=4,ensure_ascii=False))
            # End perm loop
        #end side loop
    sorder.extend(sorder_batch)
    #end card loop

print(sorder)
shuffle(sorder)
print(json.dumps(sorder,indent=4,ensure_ascii=False))


