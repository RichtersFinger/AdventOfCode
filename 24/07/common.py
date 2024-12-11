"""Common code"""

from typing import Optional, Callable
from dataclasses import dataclass
import threading
from itertools import product
from functools import reduce


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


class Queue:
    """Minimal task-queue implementation."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._queue: list[Equation] = []

    def queue(self, element: Equation) -> None:
        """Add element to queue."""
        with self._lock:
            self._queue.append(element)

    def get(self) -> Optional[Equation]:
        """Get element from queue."""
        with self._lock:
            return self._queue.pop(0)

    def __len__(self):
        return len(self._queue)


class ThreadedCalculator:
    """Threaded calculator."""

    def __init__(self, nthreads: int) -> None:
        self._nthreads = nthreads

    def _init_queue(self, data: str) -> Queue:
        """Initialize queue with Equations."""
        q = Queue()
        for e in data.strip().split("\n"):
            value, numbers = e.split(":")
            q.queue(
                Equation(
                    int(value),
                    tuple(map(int, numbers.split())),
                    (Equation.add, Equation.mul),
                )
            )
        return q

    def run(self, data: str) -> list[Equation]:
        """Execute calculation."""
        q = self._init_queue(data)

        _result = {}
        thread_pool = []
        while len(q) > 0 or len(thread_pool) > 0:
            if len(thread_pool) <= self._nthreads and len(q) > len(
                thread_pool
            ):
                thread_pool.append(
                    threading.Thread(
                        target=lambda: _result.update(
                            {threading.current_thread().native_id: [e]}
                            if (e := q.get()).solve()
                            else {}
                        ),
                        daemon=True,
                    )
                )
                thread_pool[-1].start()
            else:
                thread_pool = [t for t in thread_pool if t.is_alive()]
        return sum(_result.values(), [])
