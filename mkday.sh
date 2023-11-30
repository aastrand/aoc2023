#!/bin/bash

mkdir -p day$1
cp template.py "day${1}/day${1}.py"

# Download input
# Put this in .cookie.txt
# cookie: session=<token-copied-from-browser-devtools>
curl -o day$1/input.txt -H @.cookie.txt https://adventofcode.com/2023/day/$1/input
