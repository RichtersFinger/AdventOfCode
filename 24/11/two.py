"""Advent of Code 2024 - Day 11: Plutonian Pebbles (Part 2)"""

import one


if __name__ == "__main__":
    stones = sum(one.blink(stone, 75) for stone in one.stones)
    print(stones)
