#!/bin/bash
set -e

# stop the build if there are Python syntax errors or undefined names
flake8 --exclude template.py **/*.py --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
flake8 --exclude template.py **/*.py test* --count --max-line-length=127 --statistics
