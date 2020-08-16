import board
import digitalio
import busio
import displayio
import time

import adafruit_il0398
from babel.babelflash import FlashBabel
from adafruit_display_text import label
from adafruit_debouncer import Debouncer
from adafruit_mcp230xx.mcp23008 import MCP23008

import json
import random

# MCP Setup
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23008(i2c)
pin = mcp.get_pin(1)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.UP
switch = Debouncer(pin)

# Display Setup
displayio.release_displays()
# Reset flash pins
bcs = digitalio.DigitalInOut(board.D4)
bcs.direction = digitalio.Direction.OUTPUT
bcs.value = True
sdcs = digitalio.DigitalInOut(board.D5)
sdcs.direction = digitalio.Direction.OUTPUT
sdcs.value = True
srcs = digitalio.DigitalInOut(board.D6)
srcs.direction = digitalio.Direction.OUTPUT
srcs.value = True
# Create Screen
spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = board.A4
epd_busy = board.A3
display_bus = displayio.FourWire(spi, command=epd_dc, chip_select=epd_cs,
                                 reset=epd_reset, baudrate=1000000)
time.sleep(1)  # Wait a bit
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 400
display = adafruit_il0398.IL0398(display_bus, width=DISPLAY_WIDTH,
                                 height=DISPLAY_HEIGHT,
                                 rotation=270, busy_pin=epd_busy,
                                 highlight_color=0xFFFFFF)

# Babel Setup
babel = FlashBabel(bcs)

# Open File
data = []
with open("deck.json") as fp:
    data = json.load(fp)

# Functions:
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

def wrap_nicely(string, max_chars):
    """A helper that will return the string with word-break wrapping.
    :param str string: The text to be wrapped.
    :param int max_chars: The maximum number of characters on a line before wrapping.
    """
    string = string.replace('\n', '').replace('\r', '') # strip confusing newlines
    words = string.split(' ')
    the_lines = []
    the_line = ""
    for w in words:
        if len(the_line+' '+w) <= max_chars:
            the_line += ' '+w
        else:
            the_lines.append(the_line)
            the_line = w
    if the_line:
        the_lines.append(the_line)
    the_lines[0] = the_lines[0][1:]
    the_newline = ""
    for w in the_lines:
        the_newline += '\n'+w
    return the_newline

def wrap_kanji(string, max_chars):
    chunks = [string[i:i+max_chars] for i in range(0, len(string), max_chars)]
    my_new_list = [x + "\n" for x in chunks]
    return ''.join(my_new_list)

text = "こんにちわ!\nWelcome!"
text_group = displayio.Group(max_size=10, scale=2, x=120, y=150)
text_area = label.Label(babel.font, text=text, color=0xFF0000) #babel.font
text_group.append(text_area)
text_area.x = -50
text_area.y = 0
display.show(text_group)
display.refresh()
time.sleep(5)
while (switch.rose != True):
    switch.update()
switch.update()
print("Rose!")

while True:
    for card in data["cards"]:
        english, indexes = pick_replacements_and_index(card["e"],"e")
        kanji = match_replacements_by_index(card["k"], "k", indexes)
        hiragana = match_replacements_by_index(card["h"], "h", indexes)
        # Print English
        text = wrap_nicely(english, 18)
        text_group = displayio.Group(max_size=10, scale=2, x=120, y=150)
        text_area = label.Label(babel.font, text=text, color=0xFF0000) #babel.font
        text_group.append(text_area)
        text_area.x = -55
        text_area.y = 0
        display.show(text_group)
        display.refresh()
        time.sleep(5)
        # wait for button press
        while (switch.rose != True):
            switch.update()
        switch.update()
        print("rose!")
        text = text = wrap_nicely(english, 18) + "\n" + wrap_kanji(kanji, 8) + "\n" + wrap_kanji(hiragana, 8)
        text_group = displayio.Group(max_size=10, scale=2, x=120, y=150)
        text_area = label.Label(babel.font, text=text, color=0xFF0000) #babel.font
        text_group.append(text_area)
        text_area.x = -55
        text_area.y = 0
        display.show(text_group)
        display.refresh()
        time.sleep(5)
        # wait for button press
        while (switch.rose != True):
            switch.update()
        switch.update()
        print("rose!")
