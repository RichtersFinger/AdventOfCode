"""Advent of Code 2024 - Day 1: Historian Hysteria (Part 1)"""

import sys
from pathlib import Path


print(
    sum(  # sum up
        map(  # calculate distances
            lambda x: abs(int(x[0]) - int(x[1])),
            zip(  # recombine
                *map(  # arrange data
                    sorted,
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
            ),
        )
    )
)
