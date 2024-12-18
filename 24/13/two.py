"""Advent of Code 2024 - Day 13: Claw Contraption (Part 2)"""

import re

import one


class Machine(one.Machine):
    BTN_LIMIT = None
    PRIZE_OFFSET = 10000000000000

    def __init__(self, **kwargs: str):
        super().__init__(**kwargs)
        self.p = (self.p[0] + self.PRIZE_OFFSET, self.p[1] + self.PRIZE_OFFSET)


if __name__ == "__main__":
    print(
        sum(
            Machine.scalarproduct(instructions, (3, 1))
            for machine in one.machines
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
