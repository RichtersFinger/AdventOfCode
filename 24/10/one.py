"""Advent of Code 2024 - Day 10: Hoof It (Part 1)"""

import sys
from pathlib import Path
from dataclasses import dataclass, field


TRAIL_START = 0
TRAIL_END = 9


class Trail:
    def __init__(self, *args: tuple[int, int]):
        self.path = list(p for p in args)

    def walk(self, terrain: tuple[tuple[int, ...], ...]) -> list["Trail"]:
        current = self.path[-1]
        height = terrain[current[1]][current[0]]
        if height == TRAIL_END:
            return [Trail(*self.path)]

        options = [
            (x, y)
            for x, y in (
                (current[0] - 1, current[1]),
                (current[0] + 1, current[1]),
                (current[0], current[1] - 1),
                (current[0], current[1] + 1),
            )
            if 0 <= x < len(terrain[0])
            and 0 <= y < len(terrain)
            and terrain[y][x] == height + 1
        ]
        if not options:
            return []

        return sum(
            (Trail(*self.path, option).walk(terrain) for option in options), []
        )


@dataclass
class Trailhead:
    trails: list[Trail] = field(default_factory=list)

    def walk_all(self, terrain: tuple[tuple[int, ...], ...]) -> None:
        _trails = []
        for trail in self.trails:
            _trails.extend(trail.walk(terrain))
        self.trails = _trails

    def score(self) -> int:
        return len(set(trail.path[-1] for trail in self.trails))

    def rating(self) -> int:
        return len(self.trails)


terrain = tuple(
    map(
        lambda line: tuple(map(int, tuple(line))),
        Path(sys.argv[1]).read_text(encoding="utf-8").strip().split(),
    ),
)

trailheads = [
    Trailhead([Trail((x, y))])
    for y, row in enumerate(terrain)
    for x, value in enumerate(row)
    if value == TRAIL_START
]


for th in trailheads:
    th.walk_all(terrain)

if __name__ == "__main__":
    print(sum(th.score() for th in trailheads))
