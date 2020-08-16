# PyShuffle

PyShuffle is a basic script for creating and studying semi-randomly assembled sentences in Japanese. Using a JSON collection of "cards" and "word-lists", the program autofills categories for nouns, verbs and particles to create many variations of a single sentence for study. Many different kinds of sentences can be combined in a single deck for broad study sessions.

PyShuffle is capable of running on embedded devices such as the [OpenBook](https://github.com/joeycastillo/The-Open-Book) by using [Circuitpython](https://github.com/adafruit/circuitpython).



## 

## Getting started:

[JapaneseVerbConjugator](https://pypi.org/project/JapaneseVerbConjugator/) and [pykakasi](https://pypi.org/project/pykakasi/) are required to generate your own properly formatted word and card lists from .csv files. It is recommended to install these on a python virtual environment with tools like  [virtualenv](https://pypi.org/project/virtualenv/)/[virtualenvwrapper](https://pypi.org/project/virtualenvwrapper/).

```
workon shuffle_env
pip install romkan japaneseverbconjugator pykakasi
```

You can view example files of the correct CSV format in the `tablegen/example_files` directory. CSV files can be created by hand or found online and reformatted. Run each script by passing the target csv file:

```
python csv_to_table.py example_files/day_counters.csv
```

This will generate correctly formatted text that you can past into an appropriate "word lists" category. 

## Creating Cards and Word-Lists

The syntax of the decks.json file is very simple, containing two main groups, `word-lists` and `cards`. `word-lists` are categories of single words that are intended to replace a "token" inside a sentence - for instance, a token representing a "person" could select from words for "my father", "my friend", "Mr John Doe" or other titles. Similarly, a token for conjugated past-tense verbs could pick from "ran", "swam", "ate" etc. 

`cards` represent sentences with exchangeable tokens for words. Each token is marked with an index number to link it to the translated versions, in case tokens undergo a change in order based on language-specific grammar conventions. Each token appears in the syntax`<<#::my_wordlist>>` where the `#` indicates the linking number. For Japanese, cards consist of three separate variations of the sentence - one in English, one in kanji form, and one in hiragana form for reading practice. Each sentence must contain all tokens  included in the first. 

## Running the program

Shuffle assumes that a deck.json file exists in the same directory. Call it from a terminal with:

```
python shuffle.py
```

This will open an interactive study session. You can then select a single card from your collection to work on, or simply hit enter to have a rotating selection of all cards.

## Using Circuitpython

If you have an Open Book or similar embedded device and would like to create your own study tool, simply upload your JSON deck and the `code.py` file in the `circuitpy/` directory to your CIRCUITPY drive. The Open Book will also require the following circuitpython libraries:

- `adafruit_bitmap_font`
- `adafruit_bus_device`
- `adafruit_display_text`
- `adafruit_mcp230xx`
- `babel`
- `display_bidi_text`
- `adafruit_debouncer.mpy`
- `adafruit_il0398.py`



## Contributing

I'm far from being a python pro so this sketch is so far pretty basic. Any ideas or issue reports would be greatly appreciated!

Future goals for this project might include:

- A "tag" system for words to include them in an exchange set, rather than using word-lists, so that words do not need to be included redundantly across multiple categories that contain them. 
- More sophisticated management of tenses, such as storing verbs with all possible conjugations included. 
- Better options for study sessions, such as selecting collections of cards or specifying a certain category of word to focus on. 
- SRS features, such as storing familiarity numbers per card or per word, and storing them in a separate "metadata" file.
- While in a study session, selecting specific words out of a card for a "sub-session" of focused practice. 
- Knowledge cards for grammar linked to certain cards or categories. 
- General improvement of code quality.