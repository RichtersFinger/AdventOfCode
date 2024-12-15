"""Advent of Code 2024 - Day 7: Bridge Repair (Part 1)"""

import sys
from pathlib import Path

import common


def generate_queue(data: str) -> list[common.Equation]:
    """Generate list of Equations to solve."""
    q = []
    for e in data.strip().split("\n"):
        value, numbers = e.split(":")
        q.append(
            common.Equation(
                int(value),
                tuple(map(int, numbers.split())),
                (common.Equation.add, common.Equation.mul),
            )
        )
    return q


print(
    sum(
        e.value if e is not None else 0
        for e in common.ThreadedCalculator(16).run(
            generate_queue(
                Path(sys.argv[1]).read_text(encoding="utf-8")
            )
        )
    )
)
