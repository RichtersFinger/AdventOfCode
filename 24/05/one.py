"""Advent of Code 2024 - Day 5: Print Queue (Part 1)"""

import sys
from pathlib import Path
from re import finditer, MULTILINE


print(
    sum(  # calculate total
        map(  # get middle page number as integer
            lambda acceptable_updates: int(
                acceptable_updates[len(acceptable_updates) // 2]
            ),
            map(  # split valid updates into individual pages
                lambda acceptable_updates: acceptable_updates[1:-1].split(
                    ",,"
                ),
                *map(  # filter all updates using the regex
                    lambda x: [
                        update
                        for update in x[1].split()
                        if update
                        not in [
                            match.group()
                            for match in finditer(x[0], x[1], MULTILINE)
                        ]
                    ],
                    tuple(
                        map(
                            lambda x: (  # build regex that matches any line with bad page order
                                "|".join(
                                    map(
                                        lambda rule: rf"(^.*?,{rule[1]},.*?,{rule[0]},.*?$)",
                                        map(
                                            lambda rule_str: rule_str.split(
                                                "|"
                                            ),
                                            x[0].split(),
                                        ),
                                    )
                                ),
                                "\n".join(  # reformat updates for easier matching via regex
                                    map(
                                        lambda update: f",{update},",
                                        x[1].replace(",", ",,").split(),
                                    )
                                ),
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
)
