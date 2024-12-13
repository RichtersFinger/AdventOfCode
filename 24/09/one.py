"""Advent of Code 2024 - Day 9: Disk Fragmenter (Part 1)"""

from typing import Optional
import sys
from pathlib import Path
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Disk:
    """Software Disk."""

    blocks: list[Optional[int]] = field(default_factory=list)
    _defrag_pointer: int = 0

    def load_raw(self, raw: str) -> tuple[int]:
        """
        Writes blocks and returns maximum file id generated that way.
        """
        last_id = 0
        for id_, mode, size in map(
            lambda x: (x[0] // 2, x[0] % 2, x[1]),
            enumerate(map(int, list(raw))),
        ):
            if mode == 0:
                self.append(id_, size)
                last_id = id_
            else:
                self.expand(size)
        return last_id

    def expand(self, blocks: int) -> None:
        """Expand disk-space by `blocks`."""
        self.append(None, blocks)

    def append(self, id_: Optional[int], blocks: int) -> None:
        """Append file with `id_` of size `blocks` to disk."""
        self.blocks.extend([id_] * blocks)

    def load_fragmented(self, id_: int) -> Optional[int]:
        """
        Removes (fragmented) file from disk and returns number of
        blocks. If file does not exist, returns `None` instead.
        """
        blocks = self.blocks.count(id_)
        if blocks == 0:
            return None
        self._defrag_pointer = min(
            self._defrag_pointer, self.blocks.index(id_)
        )
        self.blocks = [None if id__ == id_ else id__ for id__ in self.blocks]
        return blocks

    def write_fragmented(self, id_: int, blocks: int) -> None:
        """
        Write file with `id_` of size `blocks` fragmented into empty
        blocks.
        """
        written = 0
        pointer = self._defrag_pointer
        while written < blocks:
            if self.blocks[pointer] is None:
                self.blocks[pointer] = id_
                written += 1
            pointer += 1
        self._defrag_pointer = pointer

    def fragmented(self) -> bool:
        """Returns `True` if disk is fragmented."""
        if len(d.blocks) < 2:
            return True
        for pointer, (block0, block1) in enumerate(
            zip(
                self.blocks[self._defrag_pointer:-1],
                self.blocks[self._defrag_pointer + 1:],
            )
        ):
            if block0 is None and block1 is not None:
                return True
            if block0 is not None:
                self._defrag_pointer = max(self._defrag_pointer, pointer)
        return False

    def checksum(self) -> int:
        """Returns checksum."""
        return sum(
            map(
                lambda x: (x[0] or 0) * x[1],
                zip(self.blocks, range(len(self.blocks))),
            )
        )


if __name__ == "__main__":
    d = Disk()

    # initialize
    last_id = d.load_raw(Path(sys.argv[1]).read_text(encoding="utf-8").strip())

    # fragment data
    for id_ in range(last_id, 0, -1):
        if not d.fragmented():
            break
        d.write_fragmented(id_, d.load_fragmented(id_))

    # output
    # print("".join(map(lambda x: "." if x is None else str(x), d.blocks)))
    print(d.checksum())
