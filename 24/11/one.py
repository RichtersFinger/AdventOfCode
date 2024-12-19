"""Advent of Code 2024 - Day 11: Plutonian Pebbles (Part 1)"""

import sys
from pathlib import Path
import math


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
    (Specialized) minimal function-cache using a dictionary.
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


def cache_list(func):
    """
    (Specialized) limited function-cache using a list (instead of dict).
    (fastest)
    """
    IMAX = 76
    NMAX = 1001
    _cache = [-1] * IMAX

    def cached_func(n, i):
        if i > IMAX or n > NMAX:
            return func(n, i)
        if i < IMAX and _cache[i] == -1:
            _cache[i] = [-1] * NMAX
        if _cache[i][n] == -1:
            _cache[i][n] = (result := func(n, i))
            return result
        return _cache[i][n]

    return cached_func


@cache_list
def blink(number: int, iterate: int) -> int:
    for i in range(iterate, 0, -1):
        if number == 0:
            number = 1
        elif (n := math.floor(math.log10(number)) + 1) % 2 == 0:
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
