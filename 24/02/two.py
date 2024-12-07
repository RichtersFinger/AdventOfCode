"""Advent of Code 2024 - Day 2: Red-Nosed Reports (Part 2)"""

import sys
from pathlib import Path


print(
    len(  # count those reports
        list(
            filter(  # filter for safe reports
                lambda x: any(
                    all(-4 < y < 0 for y in z) or all(0 < y < 4 for y in z)
                    for z in x
                ),
                map(  # calculate distance between levels
                    lambda x: map(
                        lambda z: tuple(
                            map(lambda y: (int(y[1]) - int(y[0])), z)
                        ),
                        x,
                    ),
                    map(  # duplicate with offset & zip
                        lambda x: map(lambda y: tuple(zip(y, y[1:])), x),
                        map(  # generate all report-variations
                            lambda x: tuple(
                                [x]
                                + list(
                                    [y for i, y in enumerate(x) if i != j]
                                    for j, _ in enumerate(x)
                                )
                            ),
                            map(  # parse input by line
                                lambda x: x.split(),
                                Path(sys.argv[1])
                                .read_text(encoding="utf-8")
                                .strip()
                                .split("\n"),
                            ),
                        ),
                    ),
                ),
            )
        )
    )
)
