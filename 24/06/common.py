"""Common code"""

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
        self._raw = list(map(list, data.strip().split()))
        self.guard = next(
            Guard(value, Vector(i, j))
            for j, row in enumerate(self._raw)
            for i, value in enumerate(row)
            if value in Directions
        )

    def alter(self, p: Vector, value: str) -> None:
        """Alter timeline."""
        self._raw[p.y][p.x] = value

    def run(self) -> tuple[bool, set[tuple[int, int]]]:
        """
        Run simulation, returns whether guard is trapped and a set of
        visited locations.
        """
        trapped = False
        route = set()
        direction = Directions(self.guard.s)
        next_position = self.guard.p
        while 0 <= next_position.x < len(
            self._raw[0]
        ) and 0 <= next_position.y < len(self._raw):
            if self._raw[next_position.y][next_position.x] == self.OBSTACLE:
                direction = direction.turned()
            else:
                self.guard.p = next_position
                if (
                    (p := (direction.value, self.guard.p.x, self.guard.p.y))
                    in route
                ):
                    trapped = True
                    break
                route.add(p)
            next_position = (
                self.guard.p + self.DIRECTION_INCREMENTS[direction]
            )
        return trapped, set((p[1], p[2]) for p in route)
