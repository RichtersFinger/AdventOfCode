"""Advent of Code 2024 - Day 3: Mull It Over (Part 2)"""

import sys
from pathlib import Path
from re import finditer


print(
    sum(  # sum up values
        int(instruction.groupdict()["x"]) * int(instruction.groupdict()["y"])
        for instruction in finditer(  # collect valid instructions by matching pattern
            r"mul\((?P<x>\d*),(?P<y>\d*)\)",
            "".join(  # recombine into single sequence of instructions
                sequence.group(0)
                for sequence in finditer(  # collect valid sequences by matching pattern
                    r"do\(\)[\S\s]*?don\'t\(\)",
                    f"do(){Path(sys.argv[1]).read_text(encoding='utf-8')}don't()",
                )
            ),
        )
    )
)
