#!/bin/bash

year=2023
mkdir -p day$1
cat template.py | sed s/'{{ day }}'/${1}/g > day${1}/day${1}.py
chmod +x day${1}/day${1}.py

# Download input
# Put this in .cookie.txt
# cookie: session=<token-copied-from-browser-devtools>
mkdir -p input/$year
curl -o input/$year/day$1.txt -H @.cookie.txt -A "mkday.sh by github.com/aastrand via cURL" https://adventofcode.com/$year/day/$1/input
cat input/$year/day$1.txt

cd input
git add $year/day$1.txt
git commit -am "${year} day $1"
git push origin main
cd ../day$1

open day$1.py
