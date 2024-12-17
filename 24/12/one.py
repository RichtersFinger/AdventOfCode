"""Advent of Code 2024 - Day 12: Garden Groups (Part 1)"""

import sys
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Region:
    value: str
    plot: set[tuple[int, int]] = field(default_factory=set)

    @classmethod
    def find_region(
        cls,
        garden: tuple[tuple[str, ...], ...],
        notes: set[tuple[int, int]],
        i: int,
        j: int,
        value: str,
    ) -> "Region":
        """
        Returns list of positions that are part of the region associated
        with (i, j).

        Keyword arguments:
        garden -- input data
        notes -- already visited places
        i -- x-coordinate
        j -- y-coordinate
        value -- region's id
        """
        if (i, j) in notes:
            return cls(value, {})
        result = cls(value, {(i, j)})
        notes.add((i, j))

        if i > 0 and garden[j][i - 1] == value and (i - 1, j) not in notes:
            result.plot.update(
                cls.find_region(garden, notes, i - 1, j, value).plot
            )
        if (
            i < len(garden[0]) - 1
            and garden[j][i + 1] == value
            and (i + 1, j) not in notes
        ):
            result.plot.update(
                cls.find_region(garden, notes, i + 1, j, value).plot
            )
        if j > 0 and garden[j - 1][i] == value and (i, j - 1) not in notes:
            result.plot.update(
                cls.find_region(garden, notes, i, j - 1, value).plot
            )
        if (
            j < len(garden) - 1
            and garden[j + 1][i] == value
            and (i, j + 1) not in notes
        ):
            result.plot.update(
                cls.find_region(garden, notes, i, j + 1, value).plot
            )

        return result

    @property
    def area(self) -> int:
        """Returns region's area."""
        return len(self.plot)

    @property
    def perimeter(self) -> int:
        """Returns region's perimeter."""
        neighbors = ((-1, 0), (1, 0), (0, -1), (0, 1))
        p = 0
        for x in self.plot:
            p += 4 - sum(
                tuple(sum(y) for y in zip(x, n)) in self.plot
                for n in neighbors
            )

        return p

    @property
    def price(self) -> int:
        """Returns region's price."""
        return self.area * self.perimeter


garden = tuple(
    map(
        tuple,
        Path(sys.argv[1]).read_text(encoding="utf-8").strip().split(),
    ),
)


if __name__ == "__main__":
    regions = []  # collection of plots
    garden_notes = set()  # previously visited places

    for j, row in enumerate(garden):
        for i, value in enumerate(row):
            if (
                region := Region.find_region(garden, garden_notes, i, j, value)
            ).area > 0:
                regions.append(region)

    print(sum(region.price for region in regions))
