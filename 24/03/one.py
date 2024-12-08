"""Advent of Code 2024 - Day 3: Mull It Over (Part 1)"""

import sys
from pathlib import Path
from re import finditer


print(
    sum(  # sum up values
        int(instruction.groupdict()["x"]) * int(instruction.groupdict()["y"])
        for instruction in finditer(  # collect valid instructions by matching pattern
            r"mul\((?P<x>\d*),(?P<y>\d*)\)",
            Path(sys.argv[1]).read_text(encoding="utf-8"),
        )
    )
)
