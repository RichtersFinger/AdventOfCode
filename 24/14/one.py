"""Advent of Code 2024 - Day 14: Restroom Redoubt (Part 1)"""

from typing import Optional
import sys
from pathlib import Path
import re
from dataclasses import dataclass
from functools import reduce
from operator import mul


class Robot:
    PATTERN = r"p=(?P<px>[-\+]?\d+),(?P<py>[-\+]?\d+) v=(?P<vx>[-\+]?\d+),(?P<vy>[-\+]?\d+)"

    def __init__(self, px: str, py: str, vx: str, vy: str) -> None:
        self.p = (int(px), int(py))
        self.v = (int(vx), int(vy))

    def move(self, seconds: int) -> None:
        self.p = (
            self.p[0] + seconds * self.v[0],
            self.p[1] + seconds * self.v[1],
        )


def positive_modulo(x: int, y: int) -> int:
    return ((x % y) + y) % y


@dataclass
class Room:
    w: int
    h: int

    def consider_teleports(self, robot: Robot) -> None:
        robot.p = (
            positive_modulo(robot.p[0], self.w),
            positive_modulo(robot.p[1], self.h),
        )

    def locate(self, robot: Robot) -> Optional[tuple[int, int]]:
        """Returns quadrant for robot or None if ambiguous."""
        if self.w % 2 != 0 and robot.p[0] == self.w // 2:
            return None
        if self.h % 2 != 0 and robot.p[1] == self.h // 2:
            return None
        return int(robot.p[0] > self.w // 2), int(robot.p[1] > self.h // 2)

    def map_to_quadrants(
        self, robots: list[Robot]
    ) -> list[int, int, int, int]:
        quadrants = [[0, 0], [0, 0]]
        for robot in robots:
            self.consider_teleports(robot)
            if position := self.locate(robot):
                quadrants[position[0]][position[1]] += 1
        return quadrants


robots = Path(sys.argv[1]).read_text(encoding="utf-8").strip().split("\n")


if __name__ == "__main__":
    room = Room(101, 103)
    robots = [
        Robot(**re.match(Robot.PATTERN, robot).groupdict()) for robot in robots
    ]
    for robot in robots:
        robot.move(100)

    print(reduce(mul, sum(room.map_to_quadrants(robots), [])))
