# This tool is used to create lists of verb conjugations for Japanese
# The first argument must be a csv file where each row is the format "kanji,english"
# The second argument specifies if the verbs are GODAN or ICHIDAN.
# Verbs in a file can only be of a single type.

from japaneseverbconjugator.src import \
    JapaneseVerbFormGenerator as japaneseVerbFormGenerator
from japaneseverbconjugator.src.constants.EnumeratedTypes import \
    VerbClass, Tense, Polarity, Formality
import csv
import sys
import pykakasi

FULL_LIST = True
if (sys.argv[2] == "godan"):
    VERB_CLASS = VerbClass.GODAN
elif (sys.argv[2] == "ichidan"):
    VERB_CLASS = VerbClass.ICHIDAN
else:
    raise Exception("verb class must be godan or ichidan")


kks = pykakasi.kakasi()
kks.setMode("J","H")
conv = kks.getConverter()

jvfg = japaneseVerbFormGenerator.JapaneseVerbFormGenerator()

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # k-non-past,k-non-past-polite,k-past,k-past-polite,k-te-form,k-potential,
        # k-passive,k-causative,k-causative-passive,k-imperative
        text = ""
        # non-past
        text += jvfg.generate_plain_form(row[0], VERB_CLASS, Tense.NONPAST, Polarity.POSITIVE) + ","
        text += jvfg.generate_plain_form(row[0], VERB_CLASS, Tense.NONPAST, Polarity.NEGATIVE) + ","
        # non-past-polite
        text += jvfg.generate_polite_form(row[0], VERB_CLASS, Tense.NONPAST, Polarity.POSITIVE) + ","
        text += jvfg.generate_polite_form(row[0], VERB_CLASS, Tense.NONPAST, Polarity.NEGATIVE) + ","
        # past
        text += jvfg.generate_plain_form(row[0], VERB_CLASS, Tense.PAST, Polarity.POSITIVE) + ","
        text += jvfg.generate_plain_form(row[0], VERB_CLASS, Tense.PAST, Polarity.NEGATIVE) + ","
        # past-polite
        text += jvfg.generate_polite_form(row[0], VERB_CLASS, Tense.PAST, Polarity.POSITIVE) + ","
        text += jvfg.generate_polite_form(row[0], VERB_CLASS, Tense.PAST, Polarity.NEGATIVE) + ","

        if FULL_LIST:
            # te-form
            text += jvfg.generate_te_form(row[0], VERB_CLASS) + ","
            # te-form-polite
            text += jvfg.generate_potential_form(row[0], VERB_CLASS, Formality.POLITE, Polarity.POSITIVE) + ","
            text += jvfg.generate_potential_form(row[0], VERB_CLASS, Formality.POLITE, Polarity.NEGATIVE) + ","
            # potential


        # english
        text += row[1]
        print(text)