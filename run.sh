#!/bin/bash

for d in {1..25}; do
  if [[ -e "day${d}/day${d}.py" ]]; then
    cd day$d;
    echo "Running day${d}"

    time PYTHONPATH=..:. ./day$d.py;
    r=$?
    if [ $r -ne 0 ]; then
      echo "Error running ${d}"
      exit $r
    fi

    echo ""
    cd $OLDPWD;
  fi

done
