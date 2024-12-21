"""Advent of Code 2024 - Day 15: Warehouse Woes (Part 2)"""

from typing import Optional

import one


class LBox(one.Entity):
    S = "["


class RBox(one.Entity):
    S = "]"


class GPS(one.GPS):

    @staticmethod
    def map_tile(s: str) -> Optional[one.Entity]:
        if s == "@":
            return one.Robot
        if s == "[":
            return LBox
        if s == "]":
            return RBox
        if s == "#":
            return one.Wall
        if s == ".":
            return None

    def _vmove(self, entity: Optional[one.Entity], d: one.Vector) -> None:
        # non-box cases
        if not isinstance(entity, (LBox, RBox)):
            super().move(entity, d)
            return

        # box cases
        if isinstance(entity, LBox):
            boxl = entity
            boxr = self.gps[entity.y][entity.x + 1]
        else:
            boxl = self.gps[entity.y][entity.x - 1]
            boxr = entity
        targets = (
            one.Vector(boxl.x + d.x, boxl.y + d.y),
            one.Vector(boxr.x + d.x, boxr.y + d.y),
        )

        self.move(self.gps[targets[0].y][targets[0].x], d)
        self.move(self.gps[targets[1].y][targets[1].x], d)
        self.gps[boxl.y][boxl.x] = None
        self.gps[boxr.y][boxr.x] = None
        self.gps[targets[0].y][targets[0].x] = boxl
        self.gps[targets[1].y][targets[1].x] = boxr
        boxl.x = targets[0].x
        boxl.y = targets[0].y
        boxr.x = targets[1].x
        boxr.y = targets[1].y

    def _vprobe(self, target: one.Vector, d: one.Vector) -> bool:
        # non-box cases
        entity = self.gps[target.y][target.x]
        if entity is None:
            return True

        if not isinstance(entity, (LBox, RBox)):
            return super().probe(target, d)

        # box cases
        if isinstance(entity, LBox):
            targetl = self.gps[entity.y + d.y][entity.x + d.x]
            targetr = self.gps[entity.y + d.y][entity.x + d.x + 1]
        else:
            targetl = self.gps[entity.y + d.y][entity.x + d.x - 1]
            targetr = self.gps[entity.y + d.y][entity.x + d.x]

        return (
            not targetl or self.probe(one.Vector(targetl.x, targetl.y), d)
        ) and (not targetr or self.probe(one.Vector(targetr.x, targetr.y), d))

    def probe(self, target: one.Vector, d: one.Vector) -> bool:
        if d.y == 0:
            return super().probe(target, d)
        return self._vprobe(target, d)

    def move(self, entity: Optional[one.Entity], d: one.Vector) -> None:
        if d.y == 0:
            return super().move(entity, d)
        return self._vmove(entity, d)


if __name__ == "__main__":
    gps = GPS.from_str(
        one.raw[0]
        .replace(".", "..")
        .replace("#", "##")
        .replace("O", "[]")
        .replace("@", "@.")
    )
    robot = gps.find_robot()
    for d in map(
        lambda _d: one.directions[_d], tuple(one.raw[1].replace("\n", ""))
    ):
        if gps.probe(one.Vector(robot.x + d.x, robot.y + d.y), d):
            gps.move(robot, d)
    print(gps.to_str())
    print(sum(gps.coordinates(LBox.S)))
