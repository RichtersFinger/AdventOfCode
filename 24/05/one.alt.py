"""Advent of Code 2024 - Day 5: Print Queue (Part 1)"""

import sys
from pathlib import Path


print(
    sum(  # calculate total
        map(  # get middle page number as integer
            lambda acceptable_updates: int(
                acceptable_updates[len(acceptable_updates) // 2]
            ),
            *map(  # use (lambda-function-)rules to filter updates
                lambda x: filter(
                    lambda update: all(rule(update) for rule in x[0]), x[1]
                ),
                map(  # map rules and updates independently
                    lambda x: (
                        # use rules to generate lambda-functions
                        # (which return True if update is valid)
                        tuple(
                            map(
                                lambda rule: (
                                    lambda update: rule[0] not in update
                                    or rule[1] not in update
                                    or update.index(rule[0])
                                    < update.index(rule[1])
                                ),
                                map(
                                    lambda rule_str: rule_str.split("|"),
                                    x[0].split(),
                                ),
                            )
                        ),
                        # map updates into lists of pages
                        tuple(map(lambda y: y.split(","), x[1].split())),
                    ),
                    (  # parse input as two parts: rules and updates
                        Path(sys.argv[1])
                        .read_text(encoding="utf-8")
                        .strip()
                        .split("\n\n"),
                    ),
                ),
            )
        ),
    ),
)
