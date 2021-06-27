import random
import csv
import json
import re
import sys
import itertools
import inquirer

DEBUG = False
DEBUG_LEVEL = 0 # 0 is only the basics, higher numbers = more messages

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log(pre, s, prio):
    if DEBUG and DEBUG_LEVEL >= prio:
        print(pre + ": "+ str(s))

def log_json(pre, s, prio):
    log(pre, json.dumps(s,indent=4,ensure_ascii=False), prio)

inq_theme = inquirer.themes.Default()
if len(sys.argv) > 1:
    if sys.argv[1] == "green":
        inq_theme = inquirer.themes.GreenPassion()


# Deck Sections are selectables, Categories, Pair Groups and Cards.
# Deck Categories are selectable types like Pronouns or nouns, and card
# groupings based on study topic (like lingodeer chapters).

# Parse deck file into dictionary
d_data = {} # holds the json, a dict of sections
d_section = "invalid section" # current section
d_category = "invalid category" # current category/subsection
d_catagory_readkeys = False
selectable_keys = []

group_keys = ["name","word-type","key-type","key-list"]

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    # Increment through the rows in the file, changing list levels as required
    for row in csv_reader:
        # Skip comments
        if (not row) or (row[0][:2] == "//"):
            continue
        # Change section (ie Selectables, Groups, Cards)
        if row[0][:2] == "# ":
            name = row[0][2:]
            d_data[name] = dict() # A dict of categories
            d_section = name
            continue
        # Change category (Nouns, chaper) within a section, mark to read keys next row
        if row[0][:3] == "## ":
            name = row[0][3:]
            d_data[d_section][name] = list() # A list of entries
            d_category = name
            d_catagory_readkeys = True
            continue
        # Read category keys after a category header
        if d_catagory_readkeys:
            selectable_keys = row
            # extract sideskip table
            # if d_section == "Cards":
            #     for key in selectable_keys:
            #         if key[0] == '~':
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
        elif d_section == "Cards":
            d_card = []
            for idx, side in enumerate(selectable_keys):
                d_card.append({"side_name":side,"text":row[idx]})
            # d_card["side_names"] = selectable_keys
            # d_card["sides"] = row[idx]
            d_data[d_section][d_category].append(d_card)

            # keylist = re.findall(r"\[(.*?)\]", scards[i][0]["text"])
            # for k in range(len(keylist)):
            #     keylist[k] = keylist[k].split(":")[0]
            # index = len(d_data[d_section][d_category])-1
            # d_data[d_section][d_category][index]["key-list"] = keylist

log("data", json.dumps(d_data,indent=4,ensure_ascii=False),1)

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

#DEBUG: don't want to select groups every time I run it
# study_group = d_data["Cards"].keys()

# Study group is the list of card subgroups (like textbook chapters)
log("study_group", study_group,0)

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
            # create an sorder entry with the given side

CARD_REPS = 5 # max number of repeats of a card

def get_key_permutations(keylist, requested):
    # randomize what word in the group gets picked
    maximums = [len(d_data["Groups"][item]["key-list"]) for item in keylist]
    ranges = [range(0,m) for m in maximums]
    outlist = list(itertools.product(*ranges))
    random.shuffle(outlist)
    return outlist[:requested]

# for every card
for i in range(len(scards)):
    # get a list of all keys on the card's first side
    keylist = re.findall(r"\[(.*?)\]", scards[i][0]["text"])
    for k in range(len(keylist)):
        keylist[k] = keylist[k].split(":")[0]
    log("keylist", keylist,1)
    # Get a list of permutation tuples
    perms = get_key_permutations(keylist, CARD_REPS)
    log("perms", perms,1)

    #TODO: Should probably do permutations/sides here, instead
    # because I do sides/permutations I can't add to sorder directly.
    sorder_batch = []
    for j in range(len(perms)):
        sorder_batch.append({})

    for s_idx, side in enumerate(scards[i]):
        #add some information to the card data list
        side_name = side["side_name"]

        # Obtain variation tuples
        variations = []
        varlist = re.findall(r"\[(.*?)\]", side["text"])
        for var in varlist:
            var = var.split(":")
            if len(var) == 1:
                variations.append(side_name)
            else:
                variations.append(var[1])
                log("vari",var[1],0)

        log("variations",variations,1)
        scards[i][s_idx]["variations"] = variations

        # map to the first keylist, assuming (for now) that all
        # groups are unique
        side_idx_map = []
        #todo: this needs to only take material before the ":" used in compound replacables
        new_keylist = re.findall(r"\[(.*?)\]", side["text"])
        for key in new_keylist:
            key = key.split(":")[0]
            for j in range(len(keylist)):
                if keylist[j] == key:
                    side_idx_map.append(j)
                    break
        log("side idx",side_idx_map,1)
        scards[i][s_idx]["idx_map"] = side_idx_map

        # create a side instance in sorder for every permutation
        for perm in perms:
            order_unit = {}
            order_unit["front_side"] = s_idx
            order_unit["perm"] = perm
            # convert Perms to actual indexes
            sorder.append({"card":i,"front_side":s_idx, "perm":perm})

        #end side loop
    #end card loop

def render_card_side(keylist, side, perm):
    log("SIDE", side, 0)
    frags = side["text"].split("[")
    outstring = frags[0]
    for f_idx, frag in enumerate(frags[1:]):
        # every frag but the first should start with a keystring
        frag = frag[frag.find("]")+1:]
        key = keylist[side["idx_map"][f_idx]]
        log("key", key, 0)
        group = d_data["Groups"][key]
        key_sel = group["key-list"][perm[side["idx_map"][f_idx]]]
        log("key-sel", key_sel, 0)
        sel = ""
        for selectable in d_data["Selectables"][group["word-type"]]:
            if (selectable[group["key-type"]] == key_sel):
                sel = selectable[side["variations"][f_idx]]
        outstring = outstring + sel + frag
    return outstring

log("scards", json.dumps(scards,indent=4,ensure_ascii=False),1)
random.shuffle(sorder)
log("sorder", json.dumps(sorder,indent=4,ensure_ascii=False),1)

for study in sorder:
    keylist = re.findall(r"\[(.*?)\]", scards[study["card"]][0]["text"])
    for k in range(len(keylist)):
        keylist[k] = keylist[k].split(":")[0]

    print(bcolors.OKCYAN + "\n\nFront Side:" + bcolors.ENDC)

    log("study", study, 0)
    log("keylist", keylist, 0)
    log_json("current card",scards[study["card"]],0)

    print(render_card_side(keylist, scards[study["card"]][study["front_side"]], study["perm"]))
    input()
    print(bcolors.OKGREEN + "Back Side:" + bcolors.ENDC)
    for side in scards[study["card"]]:
        print(render_card_side(keylist, side, study["perm"]))




