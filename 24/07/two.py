"""Advent of Code 2024 - Day 7: Bridge Repair (Part 2)"""

import sys
from pathlib import Path

import common


class Equation(common.Equation):
    @staticmethod
    def concat(x: int, y: int) -> int:
        """Returns concat."""
        return int(f"{x}{y}")


def generate_queue(data: str) -> list[Equation]:
    """Initialize queue with Equations."""
    q = []
    for e in data.strip().split("\n"):
        value, numbers = e.split(":")
        q.append(
            Equation(
                int(value),
                tuple(map(int, numbers.split())),
                (Equation.add, Equation.mul, Equation.concat),
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
