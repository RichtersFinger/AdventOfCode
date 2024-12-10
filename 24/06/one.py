"""Advent of Code 2024 - Day 6: Guard Gallivant (Part 1)"""

import sys
from pathlib import Path

import common

print(
    len(
        common.Simulation(Path(sys.argv[1]).read_text(encoding="utf-8")).run()[
            1
        ]
    )
)
