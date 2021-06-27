#!/bin/bash
# Reads a file of sentences, and turns them into a eng;kanji;hira table
filename=$1
while read line; do
eng=$line
jap=`trans -e bing -b en:ja "$line"`
hir=`python3 -c "import sys; import pykakasi; kks = pykakasi.kakasi(); r = kks.convert(sys.argv[1]); print(\"\".join([item['hira'] for item in r]))" "$jap"`
echo "$eng;$jap;$hir"
done < $filename