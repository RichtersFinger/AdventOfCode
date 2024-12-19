"""Advent of Code 2024 - Day 14: Restroom Redoubt (Part 2)"""

import re

import one


class Room(one.Room):
    def homogeneity(self, robots: list[one.Robot]) -> int:
        "Returns a measure for homogeneity of spatial distribution."
        mean = (
            sum(robot.p[0] for robot in robots) / len(robots),
            sum(robot.p[1] for robot in robots) / len(robots),
        )
        return sum(
            abs(mean[0] - robot.p[0]) + abs(mean[1] - robot.p[1])
            for robot in robots
        )

    def render(self, robots: list[one.Robot]) -> str:
        display = [[0 for _ in range(self.w)] for _ in range(self.h)]
        for robot in robots:
            display[robot.p[1]][robot.p[0]] += 1
        return "\n".join("".join(map(str, x)) for x in display)


if __name__ == "__main__":
    room = Room(101, 103)
    robots = [
        one.Robot(**re.match(one.Robot.PATTERN, robot).groupdict())
        for robot in one.robots
    ]
    seconds = 0
    while True:
        at_least_one = False
        while (
            not at_least_one
            # heuristic value..
            or room.homogeneity(robots) > 15000
        ):
            at_least_one = True
            for robot in robots:
                robot.move(1)
                room.consider_teleports(robot)
            seconds += 1
        print(room.render(robots))
        print(f"seconds={seconds}; homogeneity={room.homogeneity(robots)}")
        input("Press enter to continue.")
