"""Common code"""

from typing import Optional, Callable
from dataclasses import dataclass
from itertools import product
from functools import reduce
import multiprocessing


@dataclass
class Equation:
    """Record class for one equation."""

    value: int
    numbers: tuple[int, ...]
    operations: tuple[Callable[[int, int], int], ...]

    def solve(self) -> bool:
        """Try to solve equation. Returns `True` on success."""
        return (
            next(
                (
                    o
                    for o in product(
                        self.operations, repeat=len(self.numbers) - 1
                    )
                    if self.value
                    == reduce(
                        lambda a, b: b[1](a, b[0]),
                        zip(self.numbers[1:], o),
                        self.numbers[0],
                    )
                ),
                None,
            )
            is not None
        )

    @staticmethod
    def add(x: int, y: int) -> int:
        """Returns sum."""
        return x + y

    @staticmethod
    def mul(x: int, y: int) -> int:
        """Returns product."""
        return x * y


class ThreadedCalculator:
    """Threaded calculator."""

    def __init__(self, nthreads: int) -> None:
        self._nthreads = nthreads

    def _run(self, e: Equation) -> Optional[Equation]:
        """Evaluate single equation."""
        return e if e.solve() else None

    def run(self, queue: list[Equation]) -> list[bool]:
        """Execute calculation."""
        with multiprocessing.Pool(self._nthreads) as pool:
            return pool.map(self._run, queue)
