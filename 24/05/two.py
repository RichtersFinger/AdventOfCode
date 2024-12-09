"""Advent of Code 2024 - Day 5: Print Queue (Part 2)"""

import sys
from pathlib import Path
from functools import reduce


print(
    sum(  # calculate total
        map(  # get middle page number as integer
            lambda acceptable_updates: int(
                acceptable_updates[len(acceptable_updates) // 2]
            ),
            *map(  # apply fix to bad updates
                lambda x: [
                    reduce(
                        lambda u, rule_tools: (
                            u if rule_tools[0](u) else rule_tools[1](u)
                        ),
                        # start off with update, then iterate rules repeatedly
                        # until it converged (by simply repeating as often as
                        # necessary (?) in worst case)
                        (update,) + len(update) * x[0],
                    )
                    for update in x[1]
                ],
                map(
                    # use (lambda-function)-rules to filter updates
                    # and build lambda-functions to rectify updates
                    lambda x: (
                        (
                            x[0],
                            tuple(
                                update
                                for update in x[1]
                                if not all(
                                    rule_tools[0](update)
                                    for rule_tools in x[0]
                                )
                            ),
                        )
                    ),
                    map(  # map rules and updates independently
                        lambda x: (
                            # use rules to generate lambda-functions
                            # (which return True if update is valid)
                            tuple(
                                map(
                                    lambda rule: (
                                        # detect good update
                                        lambda update: rule[0] not in update
                                        or rule[1] not in update
                                        or update.index(rule[0])
                                        < update.index(rule[1]),
                                        # fix bad update
                                        lambda update: [
                                            (
                                                rule[1]
                                                if u == rule[0]
                                                else (
                                                    rule[0]
                                                    if u == rule[1]
                                                    else u
                                                )
                                            )
                                            for u in update
                                        ],
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
                ),
            ),
        ),
    )
)
