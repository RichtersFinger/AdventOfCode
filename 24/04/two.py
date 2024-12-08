"""Advent of Code 2024 - Day 4: Ceres Search (Part 2)"""

import sys
from pathlib import Path


print(
    sum(  # sum up matches
        *map(
            lambda z: tuple(
                (0 < x < len(z) - 1 and 0 < y < len(row) - 1)  # check bounds
                and (  # check one direction
                    z[x - 1][y - 1] + value + z[x + 1][y + 1]
                    in ("MAS", "SAM")
                )
                and (  # check other
                    z[x + 1][y - 1] + value + z[x - 1][y + 1]
                    in ("MAS", "SAM")
                )
                for x, row in enumerate(z)
                for y, value in enumerate(row)
            ),
            [  # wrap 2d-data into iterable (for call to map)
                tuple(
                    map(  # parse input
                        tuple,
                        Path(sys.argv[1])
                        .read_text(encoding="utf-8")
                        .strip()
                        .split(),
                    ),
                )
            ],
        )
    )
)
