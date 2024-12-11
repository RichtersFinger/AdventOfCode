"""Advent of Code 2024 - Day 7: Bridge Repair (Part 1)"""

import sys
from pathlib import Path

import common


print(
    sum(
        e.value
        for e in common.ThreadedCalculator(1).run(
            Path(sys.argv[1]).read_text(encoding="utf-8")
        )
    )
)
