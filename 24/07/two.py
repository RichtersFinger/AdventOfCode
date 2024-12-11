"""Advent of Code 2024 - Day 7: Bridge Repair (Part 2)"""

import sys
from pathlib import Path

import common


class Equation(common.Equation):
    @staticmethod
    def concat(x: int, y: int) -> int:
        """Returns concat."""
        return int(f"{x}{y}")


class ThreadedCalculator(common.ThreadedCalculator):
    def _init_queue(self, data: str) -> common.Queue:
        """Initialize queue with Equations."""
        q = common.Queue()
        for e in data.strip().split("\n"):
            value, numbers = e.split(":")
            q.queue(
                Equation(
                    int(value),
                    tuple(map(int, numbers.split())),
                    (Equation.add, Equation.mul, Equation.concat),
                )
            )
        return q


print(
    sum(
        e.value
        for e in ThreadedCalculator(16).run(
            Path(sys.argv[1]).read_text(encoding="utf-8")
        )
    )
)
