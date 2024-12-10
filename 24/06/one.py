"""Advent of Code 2024 - Day 6: Guard Gallivant (Part 1)"""

import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass


class Directions(Enum):
    """Directions."""

    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def turned(self) -> "Directions":
        """New direction turned clockwise."""
        order = [self.UP, self.RIGHT, self.DOWN, self.LEFT, self.UP]
        return order[order.index(self) + 1]


@dataclass
class Vector:
    """2d vector on integer-space."""

    x: int
    y: int

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)


@dataclass
class Guard:
    """Guard record class."""

    s: str
    p: Vector


class Simulation:
    """Guard movement simulation."""

    DIRECTION_INCREMENTS = {
        Directions.UP: Vector(0, -1),
        Directions.DOWN: Vector(0, 1),
        Directions.LEFT: Vector(-1, 0),
        Directions.RIGHT: Vector(1, 0),
    }
    OBSTACLE = "#"

    def __init__(self, data: str) -> None:
        self._raw = tuple(map(tuple, data.strip().split()))
        self._guard = next(
            Guard(value, Vector(i, j))
            for j, row in enumerate(self._raw)
            for i, value in enumerate(row)
            if value in Directions
        )

    def run(self) -> int:
        """Run simulation."""
        route = {(self._guard.p.x, self._guard.p.y)}
        direction = Directions(self._guard.s)
        next_position = self._guard.p
        while (
            0 <= next_position.x < len(self._raw[0])
            and 0 <= next_position.y < len(self._raw)
        ):
            if self._raw[next_position.y][next_position.x] == self.OBSTACLE:
                direction = direction.turned()
            else:
                self._guard.p = next_position
                route.add((self._guard.p.x, self._guard.p.y))
            next_position = (
                self._guard.p + self.DIRECTION_INCREMENTS[direction]
            )
        return len(route)


print(
    Simulation(Path(sys.argv[1]).read_text(encoding="utf-8")).run()
)
