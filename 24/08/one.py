"""Advent of Code 2024 - Day 8: Resonant Collinearity (Part 1)"""

import sys
from pathlib import Path
from itertools import permutations


# pre-process data
raw = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
ny = len(lines := raw.split())
nx = len(lines[0])


# find antenna-groups
antenna_groups = {
    f: tuple(
        (i, j)
        for j, row in enumerate(map(tuple, lines))
        for i, value in enumerate(row)
        if value == f
    )
    for f in set(raw.replace("\n", "").replace(".", ""))
}


# find resonances as permutations within antenna-group
resonances = sum(
    (
        list(permutations(antenna_group, 2))
        for antenna_group in antenna_groups.values()
    ),
    [],
)


# apply the relative vector per resonance
antinodes = set(
    filter(
        lambda a: 0 <= a[0] < nx and 0 <= a[1] < ny,
        ((2 * r[0][0] - r[1][0], 2 * r[0][1] - r[1][1]) for r in resonances),
    )
)


if __name__ == "__main__":
    print(len(antinodes))
