"""Advent of Code 2024 - Day 4: Ceres Search (Part 1)"""

import sys
from pathlib import Path


print(
    sum(  # overall
        map(  # count hits
            lambda variant: sum(
                line.count("XMAS") + line.count("SAMX") for line in variant
            ),
            *map(
                # map into variations (where XMAS appears in individual lines)
                lambda lines: (
                    (
                        lines,  # unaltered
                        list("".join(y) for y in zip(*lines)),  # transposed
                        list(
                            "".join(y)
                            for y in zip(
                                *list(
                                    (len(z) - i - 1) * "-" + z + i * "-"
                                    for i, z in enumerate(lines)
                                )
                            )
                        ),  # sheared -1 & transposed
                        list(
                            "".join(y)
                            for y in zip(
                                *list(
                                    i * "-" + z + (len(z) - i - 1) * "-"
                                    for i, z in enumerate(lines)
                                )
                            )
                        ),  # sheared +1 & transposed
                    )
                ),
                (  # parse input
                    Path(sys.argv[1])
                    .read_text(encoding="utf-8")
                    .strip()
                    .split(),
                ),
            ),
        )
    )
)
