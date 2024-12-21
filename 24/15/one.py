"""Advent of Code 2024 - Day 15: Warehouse Woes (Part 1)"""

from typing import Optional
import sys
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Vector:
    x: int
    y: int


directions = {
    "<": Vector(-1, 0),
    "v": Vector(0, 1),
    ">": Vector(1, 0),
    "^": Vector(0, -1),
}


@dataclass
class Entity:
    S = "?"
    MOVABLE = True
    x: int
    y: int


class Robot(Entity):
    S = "@"


class Box(Entity):
    S = "O"


class Wall(Entity):
    S = "#"
    MOVABLE = False


@dataclass
class GPS:
    w: int
    h: int
    gps: list[list[Optional[Entity]]]

    @staticmethod
    def map_tile(s: str) -> Optional[Entity]:
        if s == "@":
            return Robot
        if s == "O":
            return Box
        if s == "#":
            return Wall
        if s == ".":
            return None

    @classmethod
    def from_str(cls, raw: str) -> "GPS":
        lines = raw.split()
        return cls(
            w=len(lines[0]),
            h=len(lines),
            gps=[
                [
                    None if (tile := cls.map_tile(s)) is None else tile(x, y)
                    for x, s in enumerate(tuple(line))
                ]
                for y, line in enumerate(lines)
            ],
        )

    def to_str(self) -> str:
        return "\n".join(
            "".join("." if tile is None else tile.S for tile in row)
            for row in self.gps
        )

    def probe(self, target: Vector, d: Vector) -> bool:
        if self.gps[target.y][target.x] is None:
            return True
        if self.gps[target.y][target.x].MOVABLE and self.probe(
            Vector(target.x + d.x, target.y + d.y), d
        ):
            return True
        return False

    def move(self, entity: Optional[Entity], d: Vector) -> None:
        """Any moves need to be probed first."""
        if entity is None or not entity.MOVABLE:
            return
        target = Vector(entity.x + d.x, entity.y + d.y)

        self.move(self.gps[target.y][target.x], d)
        self.gps[entity.y][entity.x] = None
        self.gps[target.y][target.x] = entity
        entity.x = target.x
        entity.y = target.y

    def find_robot(self) -> Optional[Robot]:
        for row in self.gps:
            for e in row:
                if e is not None and e.S == Robot.S:
                    return e
        return None

    def coordinates(self, s: str) -> list[int]:
        coordinates = []
        for row in self.gps:
            for e in row:
                if e is not None and e.S == s:
                    coordinates.append(100 * e.y + e.x)
        return coordinates


raw = tuple(
    Path(sys.argv[1]).read_text(encoding="utf-8").strip().split("\n\n"),
)


if __name__ == "__main__":
    gps = GPS.from_str(raw[0])
    robot = gps.find_robot()
    for d in map(lambda _d: directions[_d], tuple(raw[1].replace("\n", ""))):
        if gps.probe(Vector(robot.x + d.x, robot.y + d.y), d):
            gps.move(robot, d)
    print(gps.to_str())
    print(sum(gps.coordinates(Box.S)))
