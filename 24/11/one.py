"""Advent of Code 2024 - Day 11: Plutonian Pebbles (Part 1)"""

import sys
from pathlib import Path


def cache(func):
    """(General) minimal function-cache for positional args."""
    _cache = {}

    def cached_func(*args):
        if args not in _cache:
            _cache[args] = (result := func(*args))
            return result
        return _cache[args]

    return cached_func


def cache_specialized(func):
    """
    (Specialized) minimal function-cache for positional args.
    (even faster)
    """
    _cache = {}

    def cached_func(n, i):
        if i not in _cache:
            _cache[i] = {}
        if n not in _cache[i]:
            _cache[i][n] = (result := func(n, i))
            return result
        return _cache[i][n]

    return cached_func


@cache_specialized
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
