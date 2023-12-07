#!/bin/bash

year=2023
mkdir -p day$1
cat template.py | sed s/'{{ day }}'/${1}/g > day${1}/day${1}.py

# Download input
# Put this in .cookie.txt
# cookie: session=<token-copied-from-browser-devtools>
mkdir -p ../aoc-input/$year
curl -o ../aoc-input/$year/day$1.txt -H @.cookie.txt -A "mkday.sh by github.com/aastrand via cURL" https://adventofcode.com/$year/day/$1/input
cat ../aoc-input/$year/day$1.txt 