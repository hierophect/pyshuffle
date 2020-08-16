from japaneseverbconjugator.src import \
    JapaneseVerbFormGenerator as japaneseVerbFormGenerator
from japaneseverbconjugator.src.constants.EnumeratedTypes import \
    VerbClass, Tense, Polarity
import csv
import sys
import pykakasi
kks = pykakasi.kakasi()
kks.setMode("J","H")
conv = kks.getConverter()

jvfg = japaneseVerbFormGenerator.JapaneseVerbFormGenerator()

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    print("PRESENT----\n")
    for row in csv_reader:
        english = row[3]
        if row[0] != "NA":
            kanji = jvfg.generate_plain_form(row[0], VerbClass.GODAN, Tense.NONPAST, Polarity.POSITIVE)
        else:
            kanji = jvfg.generate_plain_form(row[1], VerbClass.GODAN, Tense.NONPAST, Polarity.POSITIVE)
        hira = conv.do(kanji)
        print(f"{{\"e\":\"{english}\",\"h\":\"{hira}\",\"k\":\"{kanji}\"}},")

    csv_file.seek(0)
    print("POLITE PRESENT----\n")
    for row in csv_reader:
        english = row[3]
        if row[0] != "NA":
            kanji = jvfg.generate_polite_form(row[0], VerbClass.GODAN, Tense.NONPAST, Polarity.POSITIVE)
        else:
            kanji = jvfg.generate_polite_form(row[1], VerbClass.GODAN, Tense.NONPAST, Polarity.POSITIVE)
        hira = conv.do(kanji)
        print(f"{{\"e\":\"{english}\",\"h\":\"{hira}\",\"k\":\"{kanji}\"}},")

    csv_file.seek(0)
    print("PAST----\n")
    for row in csv_reader:
        english = row[3]
        if row[0] != "NA":
            kanji = jvfg.generate_plain_form(row[0], VerbClass.GODAN, Tense.PAST, Polarity.POSITIVE)
        else:
            kanji = jvfg.generate_plain_form(row[1], VerbClass.GODAN, Tense.PAST, Polarity.POSITIVE)
        hira = conv.do(kanji)
        print(f"{{\"e\":\"{english}\",\"h\":\"{hira}\",\"k\":\"{kanji}\"}},")

    csv_file.seek(0)
    print("POLITE PAST----\n")
    for row in csv_reader:
        english = row[3]
        if row[0] != "NA":
            kanji = jvfg.generate_polite_form(row[0], VerbClass.GODAN, Tense.PAST, Polarity.POSITIVE)
        else:
            kanji = jvfg.generate_polite_form(row[1], VerbClass.GODAN, Tense.PAST, Polarity.POSITIVE)
        hira = conv.do(kanji)
        print(f"{{\"e\":\"{english}\",\"h\":\"{hira}\",\"k\":\"{kanji}\"}},")