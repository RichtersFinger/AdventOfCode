"""Advent of Code 2024 - Day 11: Plutonian Pebbles (Part 1)"""

import sys
from pathlib import Path
from functools import cache


@cache
def blink(number: int, iterate: int) -> int:
    for i in range(iterate, 0, -1):
        if number == 0:
            number = 1
        elif (n := len(str(number))) % 2 == 0:
            return blink(number // (exp := 10 ** (n // 2)), i - 1) + blink(
                number % exp, i - 1
            )
        else:
            number *= 2024
    return 1


stones = [
    int(x)
    for x in Path(sys.argv[1]).read_text(encoding="utf-8").strip().split()
]

if __name__ == "__main__":
    stones = sum(blink(stone, 25) for stone in stones)
    print(stones)
