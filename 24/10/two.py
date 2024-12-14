"""Advent of Code 2024 - Day 10: Hoof It (Part 2)"""

import one


if __name__ == "__main__":
    print(sum(th.rating() for th in one.trailheads))
