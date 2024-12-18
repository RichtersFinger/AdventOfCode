"""Advent of Code 2024 - Day 13: Claw Contraption (Part 1)"""

from typing import Optional
import sys
from pathlib import Path
import re
from math import floor


class Machine:
    PATTERN = (
        r"Button A: X(?P<Ax>[-\+]?\d+), Y(?P<Ay>[-\+]?\d+)\n"
        + r"Button B: X(?P<Bx>[-\+]?\d+), Y(?P<By>[-\+]?\d+)\n"
        + r"Prize: X=(?P<Px>[-\+]?\d+), Y=(?P<Py>[-\+]?\d+)"
    )
    EPSILON = 0.001
    BTN_LIMIT = 100

    def __init__(self, **kwargs: str):
        self.a = (int(kwargs["Ax"]), int(kwargs["Ay"]))
        self.b = (int(kwargs["Bx"]), int(kwargs["By"]))
        self.babs2 = self.scalarproduct(self.b, self.b)
        self.bnorm = (-self.b[1], self.b[0])
        self.p = (int(kwargs["Px"]), int(kwargs["Py"]))

    @staticmethod
    def scalarproduct(x: tuple[int, int], y: tuple[int, int]) -> int:
        return x[0] * y[0] + x[1] * y[1]

    def solve(self) -> Optional[tuple[int, int]]:
        """
        Find linear decomposition by finding the number of a-pushes
        needed to reach the point x = n_a a, where (p - x)*b_n = 0.
        """
        _na = self.scalarproduct(self.p, self.bnorm) / self.scalarproduct(
            self.a, self.bnorm
        )
        na = floor(_na + 0.5)
        if abs(na - _na) > self.EPSILON or (
            self.BTN_LIMIT is not None and abs(na) >= self.BTN_LIMIT
        ):
            return None
        _nb = (
            self.scalarproduct(
                (self.p[0] - na * self.a[0], self.p[1] - na * self.a[1]),
                self.b,
            )
            / self.babs2
        )
        nb = floor(_nb + 0.5)
        if abs(nb - _nb) > self.EPSILON or (
            self.BTN_LIMIT is not None and abs(nb) >= self.BTN_LIMIT
        ):
            return None
        return na, nb


machines = Path(sys.argv[1]).read_text(encoding="utf-8").strip().split("\n\n")


if __name__ == "__main__":
    print(
        sum(
            Machine.scalarproduct(instructions, (3, 1))
            for machine in machines
            if (
                instructions := Machine(
                    **re.match(
                        Machine.PATTERN,
                        machine,
                        re.MULTILINE,
                    ).groupdict()
                ).solve()
            )
            is not None
        )
    )
