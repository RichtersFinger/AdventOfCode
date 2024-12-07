"""Advent of Code 2024 - Day 1: Historian Hysteria (Part 2)"""

import sys
from pathlib import Path
from functools import reduce


print(
    sum(  # sum up
        reduce(  # find scores
            lambda a, b: [int(value) * b.count(value) for value in a],
            zip(  # parse input
                *map(
                    lambda x: x.split(),
                    Path(sys.argv[1])
                    .read_text(encoding="utf-8")
                    .strip()
                    .split("\n"),
                )
            ),
        )
    )
)
