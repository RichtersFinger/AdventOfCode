"""Advent of Code 2024 - Day 2: Red-Nosed Reports (Part 1)"""

import sys
from pathlib import Path


print(
    len(  # count those reports
        list(
            filter(  # filter for safe reports
                lambda x: (
                    all(-4 < y < 0 for y in x) or all(0 < y < 4 for y in x)
                ),
                map(  # calculate distance between levels
                    lambda x: tuple(map(lambda y: (int(y[1]) - int(y[0])), x)),
                    map(  # duplicate with offset & zip
                        lambda x: tuple(zip(x, x[1:])),
                        map(  # parse input by line
                            lambda x: x.split(),
                            Path(sys.argv[1])
                            .read_text(encoding="utf-8")
                            .strip()
                            .split("\n"),
                        ),
                    ),
                ),
            )
        )
    )
)
