import json
import random

def pick_replacements_and_index(instring, lang_code):
    # Pick some replacements for a given card
    frag_list = instring.split("<<")
    indexes = [0] * len(frag_list)
    for i in range(len(frag_list)):
        # Find if a fragment starts with a replacable item
        # Todo: this should be every item except the first, right?
        if frag_list[i].find(">>") != -1:
            fragment = frag_list[i].split(">>")
            item_index = int((fragment[0].split("::"))[0]) - 1
            item_name = (fragment[0].split("::"))[1]
            insert = "NOTFOUND"

            # Pick a random item and record its index
            for category in data["word-lists"]:
                if category["name"] == item_name:
                    # pick a random index
                    rand = random.randrange(len(category["entries"]))
                    # store it
                    indexes[item_index] = rand
                    # grab the insert string
                    insert = category["entries"][rand][lang_code]

            #replace fragment with new entry
            frag_list[i] = insert + fragment[1]
    return ''.join(frag_list), indexes

def match_replacements_by_index(instring, lang_code, indexes):
    frag_list = instring.split("<<")
    for i in range(len(frag_list)):
        # Find if a fragment starts with a replacable item
        if frag_list[i].find(">>") != -1:
            fragment = frag_list[i].split(">>")
            item_index = int((fragment[0].split("::"))[0]) - 1
            item_name = (fragment[0].split("::"))[1]
            insert = "NOTFOUND"

            # For the given item, pick the correct word for the slot
            for category in data["word-lists"]:
                if category["name"] == item_name:
                    insert = category["entries"][indexes[item_index]][lang_code]

            #replace fragment with new entry
            frag_list[i] = insert + fragment[1]
    return ''.join(frag_list)


data = []
with open("deck.json") as fp:
    data = json.load(fp)

intest = input("Input card for focused study, or just enter for all cards...")

while True:
    if not intest:
        for card in data["cards"]:
            english, indexes = pick_replacements_and_index(card["e"],"e")
            kanji = match_replacements_by_index(card["k"], "k", indexes)
            hiragana = match_replacements_by_index(card["h"], "h", indexes)

            print(english)
            input("Press Enter to continue...")
            print(kanji)
            print(hiragana)
            print("\n")
    else:
        card = data["cards"][int(intest)]
        english, indexes = pick_replacements_and_index(card["e"],"e")
        kanji = match_replacements_by_index(card["k"], "k", indexes)
        hiragana = match_replacements_by_index(card["h"], "h", indexes)

        print(english)
        input("Press Enter to continue...")
        print(kanji)
        print(hiragana)
        print("\n")

