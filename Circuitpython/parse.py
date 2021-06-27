import csv
import json
import re
import sys

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
        if (not row) or (row[0][:2] == "//"):
            continue
        # Change section
        if row[0][:2] == "# ":
            name = row[0][2:]
            d_data[name] = dict() # A dict of categories
            d_section = name
            continue
        # Change category within a section, mark to read keys next row
        if row[0][:3] == "## ":
            name = row[0][3:]
            d_data[d_section][name] = list() # A list of entries
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
        elif d_section == "Cards":
            d_card = []
            for idx, side in enumerate(selectable_keys):
                d_card.append({"side_name":side,"text":row[idx]})
            # d_card["side_names"] = selectable_keys
            # d_card["sides"] = row[idx]
            d_data[d_section][d_category].append(d_card)

print(json.dumps(d_data,indent=4,ensure_ascii=False))
