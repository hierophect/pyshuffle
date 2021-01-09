# PyShuffle

PyShuffle is an application for creating and studying randomly assembled sentences in other languages. The program creates a deck of unique flashcards by replacing sections of "card templates" with semi-random verbs, nouns, and other grammar atomics. The goal is to allow language learners to use a fairly short deck of templates to study large numbers of different vocabulary items, without overstudying any single "version" of a sentence.

## Requirements

This program requires [inquirer](https://pypi.org/project/inquirer/). It can be installed with `pip install inquirer`. Windows is not supported.

The Japanese verb conjugation tool in `tools/` also requires the [JapaneseVerbConjugator](https://pypi.org/project/JapaneseVerbConjugator/) and [pykakasi](https://pypi.org/project/pykakasi/).

```
pip install romkan japaneseverbconjugator pykakasi
```

## Getting Started

Run pyshuffle by passing the location of the deck as an argument:

```
python3 pyshuffle decks/japanese_basic.csv
```

The program will show a list of chapters. Select the desired chapters with the spacebar, and hit enter to begin a flashcard studying session.

## Creating Cards and Word-Lists

The **Deck file** uses a custom syntax inspired by Markdown. This was designed to make it easier to focus on writing cards without dealing with the syntax of storage formats like JSON or XML.

It contains card templates, vocabulary, and rules for how **Replacables** (tokens within a card template) are replaced with **Selectables** (words associated with those tokens). For instance, a token representing a "person" could select from words for "my father", "my friend", "Mr John Doe" or other titles. Similarly, a token for "conjugated past-tense verb" could pick from "ran", "swam", "ate" etc. This allows many card variations to be represented by comparatively short lists of templates and vocabulary.

Decks are split into several sections:

 - **Selectables**: tables of vocabulary that include both translations and conjugation. Selectables can be broken into different subcategories, like Nouns, Verbs and Adjectives. Selectables are collections of **Variants**, the different versions of a word. Some subcategories may have more varients than others: for instance, a verb may have various different kinds of conjugations that require a long list of variants, whereas a noun may only have English and translated variants.
 - **Groups**: tables that associate a list of Selectables with a name, so they can be used within a Replacable token. This is used to narrow down the list of vocabulary that can be accessed by a card (there aren't many sentence templates that make sense with *every* verb in a language). Examples might include "things to do in a park" or "types of animals". Groups also include the information needed to search for and select the Selectables they contain, to reduce the amount of information needed in each card token.
 - **Cards**: these are card templates used to create a new "deck" every time the user starts the program. The text of the cards contains Replaceables, which are tokens indicated by square brackets `[]` that specify a Group from which to draw random vocabulary. The "sides" of a card typically correspond to the different translations of a sentence, and adjust the content and order of the Replacables automatically.

A simple example of these sections in action:
 - A card contains a simple sentence, "I saw an [animal] at the [location]", with both English and Japanese sides.
 - There are two replacables in this sentence, [animal] and [location]. Each of these corresponds to a group in the Group section. The "animal" group contains the words "dog", "cat" and "snake", and the "location" group contains "park" and "zoo".
 - In the Selectables section, "dog", "cat", "snake", "park" and "zoo" are all listed as nouns. Each of them has an English and Japanese translation.
 - When the card is presented to the user, random entries for each replacable are selected from the appropriate groups. The final translation is "I saw a dog a the park", which when "turned over" shows "公園で犬を見た", the corresponding Japanese translation using the same words.

 You can view a more comprehensive example in the `decks/japanese_basic.csv` deck. This includes more complex syntax like specifying the Variant of a word inside Replacable tokens, which is often required for verbs.


## Contributing

Contributions of any kind are welcomed. If you have a question or comment about this project that is not appropriate for a Github issue, feel free to reach out to me directly at hierophect@gmail.com or on twitter at @Hierophect.

**Upcoming features I would like to add:**

 - [ ] A GUI option for less technical users, probably starting with [PySimpleGui](https://pypi.org/project/PySimpleGUI/)
 - [ ] [Spaced Repetition](https://en.wikipedia.org/wiki/Spaced_repetition) features similar to Anki. This is complicated a bit by the fact that cards aren't unique, and thus would require extra features to help users pick distinguish what "part" of a card was forgotten.
 - [ ] Additional syntax to separate vocabular into "chapters", making it easier to group vocab from language textbooks.
 - [ ] New syntax options for things that will currently confuse the parser, such as including two groups of the same name in a card, or using words with multiple meanings/translations.
 - [ ] Possibly some overarching special-case handler that can run regexes or user-defined functions after a card is generated, handling odds and ends like the English "a" vs "an" convention.
 - [ ] A whole new "Pair Groups" section that allows certain words to always be paired with one another. Ex, "hard" and "soft" adjectives with associated lists of hard and soft nouns to describe, for use within the same "object is adj" template.

