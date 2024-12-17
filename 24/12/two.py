"""Advent of Code 2024 - Day 12: Garden Groups (Part 2)"""

from dataclasses import dataclass

import one


@dataclass
class Edge:
    p0: tuple[int, int]
    d: tuple[int, int]


@dataclass
class Region(one.Region):
    @property
    def sides(self) -> int:
        """Returns region's sides."""

        # find segments
        neighbors = ((-1, 0), (0, 1), (1, 0), (0, -1))
        # positive rotation in 2d plane
        edge_directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        edge_offsets = ((0, 0), (0, 1), (1, 1), (1, 0))
        edges = []
        for x in self.plot:
            for n, d, o in zip(neighbors, edge_directions, edge_offsets):
                if tuple(sum(y) for y in zip(x, n)) in self.plot:
                    continue
                edges.append(Edge(tuple(sum(y) for y in zip(x, o)), d))

        # trace contour and count changes of direction
        visited_edges = []
        turns = 0
        while len(visited_edges) < len(edges):
            e0 = next(e for e in edges if e not in visited_edges)
            e1 = None
            while e1 is None or e0.p0 != e1.p0:
                if e1 is None:
                    e1 = e0
                visited_edges.append(e1)

                # prioritize turning left
                next_p = next(
                    (
                        e
                        for e in edges
                        if
                        # matching end + start
                        e.p0 == tuple(sum(x) for x in zip(e1.p0, e1.d))
                        # straight or left
                        and e.d in (e1.d, (e1.d[1], -e1.d[0]))
                    ),
                    None,
                ) or next(
                    e
                    for e in edges
                    if
                    # matching end + start
                    e.p0 == tuple(sum(x) for x in zip(e1.p0, e1.d))
                    # right
                    and e.d == (-e1.d[1], e1.d[0])
                )

                if next_p.d != e1.d:
                    turns += 1
                e1 = next_p

        return turns

    @property
    def price(self) -> int:
        """Returns region's price."""
        return self.area * self.sides


if __name__ == "__main__":
    regions = []  # collection of plots
    garden_notes = set()  # previously visited places

    for j, row in enumerate(one.garden):
        for i, value in enumerate(row):
            if (
                region := Region.find_region(
                    one.garden, garden_notes, i, j, value
                )
            ).area > 0:
                regions.append(region)

    print(sum(region.price for region in regions))
