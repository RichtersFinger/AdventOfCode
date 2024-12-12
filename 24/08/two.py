"""Advent of Code 2024 - Day 8: Resonant Collinearity (Part 2)"""

from one import nx, ny, resonances


# apply the relative vector many times instead of once
antinodes = set(
    filter(
        lambda a: 0 <= a[0] < nx and 0 <= a[1] < ny,
        (
            (
                r[0][0] + n * (r[0][0] - r[1][0]),
                r[0][1] + n * (r[0][1] - r[1][1]),
            )
            for r in resonances
            for n in range(max(nx, ny))  # typically gross overestimation..
        ),
    )
)


if __name__ == "__main__":
    print(len(antinodes))
