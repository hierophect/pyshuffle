import gc
print("Pre-import memory" + str(gc.mem_free()))

import random
import json
import re
from adafruit_itertools.adafruit_itertools import product

# ------------------------------------
# Hardware setup
# ------------------------------------

import os
import board
import sdioio
import storage
import displayio
import framebufferio
import sharpdisplay
#from adafruit_display_shapes.rect import Rect
from babel.babel import Babel
from adafruit_display_text.label import Label

# Seed random
seed = hash(os.urandom(30))
print(seed)
random.seed(seed)

# Display
displayio.release_displays()
bus = board.SPI()
chip_select_pin = board.RX
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, 400, 240)
display = framebufferio.FramebufferDisplay(framebuffer)

# SD Card
sd = sdioio.SDCard(
    clock=board.SDIO_CLOCK,
    command=board.SDIO_COMMAND,
    data=board.SDIO_DATA,
    frequency=25000000)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')

# Babel
babel = Babel('/sd/babel.bin')

label = Label(font=babel.font, text=" "*40, x=20, y=120, scale=2, line_spacing=1.2, color=0, background_color=0xFFFFFF)
#background = Rect(0, 0, 400, 240, fill=0xFFFFFF)
group = displayio.Group(max_size=25)
#group.append(background)
group.append(label)
display.show(group)

print("Memory at startup:" + str(gc.mem_free()))

# ------------------------------------
# Study Setup (hardware independent)
# ------------------------------------

DECKNAME="deck.json"

def cpy_findall(regex,istring):
    outlist = []
    match = re.search(regex,istring)
    while (match):
        outlist.append(match.group(1))
        istring = istring[match.end():]
        match = re.search(regex,istring)
    return outlist

def cpy_shuffle(inlist):
    outlist = sorted(inlist, key=lambda _: random.random())
    return outlist

# Open JSON File (can't load CSVs with Circuitpython)
d_data = []
with open(DECKNAME) as fp:
    d_data = json.load(fp)

# Select all groups until I can replace the Inquirer prompt with menu
study_group = d_data["Cards"].keys()

# Study group is the list of card subgroups (like textbook chapters)
print("Study_group: " + str(study_group))

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
    outlist = list(product(*ranges))
    cpy_shuffle(outlist)
    return outlist[:requested]

# for every card
for i in range(len(scards)):
    # get a list of all keys on the card's first side
    keylist = cpy_findall(r"\[(.*?)\]", scards[i][0]["text"])
    for k in range(len(keylist)):
        keylist[k] = keylist[k].split(":")[0]
    # Get a list of permutation tuples
    perms = get_key_permutations(keylist, CARD_REPS)

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
        varlist = cpy_findall(r"\[(.*?)\]", side["text"])
        for var in varlist:
            var = var.split(":")
            if len(var) == 1:
                variations.append(side_name)
            else:
                variations.append(var[1])

        scards[i][s_idx]["variations"] = variations

        # map to the first keylist, assuming (for now) that all
        # groups are unique
        side_idx_map = []
        #todo: this needs to only take material before the ":" used in compound replacables
        new_keylist = cpy_findall(r"\[(.*?)\]", side["text"])
        for key in new_keylist:
            key = key.split(":")[0]
            for j in range(len(keylist)):
                if keylist[j] == key:
                    side_idx_map.append(j)
                    break
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
    frags = side["text"].split("[")
    outstring = frags[0]
    for f_idx, frag in enumerate(frags[1:]):
        # every frag but the first should start with a keystring
        frag = frag[frag.find("]")+1:]
        key = keylist[side["idx_map"][f_idx]]
        group = d_data["Groups"][key]
        key_sel = group["key-list"][perm[side["idx_map"][f_idx]]]
        sel = ""
        for selectable in d_data["Selectables"][group["word-type"]]:
            if (selectable[group["key-type"]] == key_sel):
                sel = selectable[side["variations"][f_idx]]
        outstring = outstring + sel + frag
    return outstring

# ------------------------------------
# Study Interface
# ------------------------------------

cpy_shuffle(sorder)

print("Memory pre-study:" + str(gc.mem_free()))

for study in sorder:
    keylist = cpy_findall(r"\[(.*?)\]", scards[study["card"]][0]["text"])
    for k in range(len(keylist)):
        keylist[k] = keylist[k].split(":")[0]

    print("Current memory:" + str(gc.mem_free()))
    print("\n\nFront Side:")

    label.text = ""
    side_text = render_card_side(keylist, scards[study["card"]][study["front_side"]], study["perm"])
    print(side_text)
    label.text = side_text
    input()
    print("Back Side:")
    for side in scards[study["card"]]:
        print(render_card_side(keylist, side, study["perm"]))


