"""Advent of Code 2024 - Day 9: Disk Fragmenter (Part 2)"""

from typing import Optional
import sys
from pathlib import Path
from dataclasses import dataclass

import one


@dataclass
class Disk(one.Disk):
    """Disk software."""

    def scan_size(self, id_: int) -> Optional[int]:
        """
        Find file size via id_ (or None if not found).
        """
        return self.blocks.count(id_)

    def scan_location(self, id_: int) -> Optional[int]:
        """
        Find file size via id_ (or None if not found).
        """
        try:
            return self.blocks.index(id_)
        except ValueError:
            return None

    def find_empty_block(self, blocks: int, max_block: int) -> Optional[int]:
        """
        Returns position of first sequence of empty blocks with given
        size `blocks` or None if none is available.
        """
        if len(self.blocks) == 0:
            return None
        try:
            pointer = self.blocks.index(None) - 1
        except ValueError:
            return None
        for running_pointer, block in enumerate(
            self.blocks[pointer:max_block], start=pointer
        ):
            if block is not None:
                pointer = running_pointer
                continue
            if running_pointer - pointer >= blocks:
                return pointer + 1
        return None

    def write_at(self, id_: Optional[int], block: int, blocks: int) -> None:
        """Write file with `id_` of size `blocks` to `block`."""
        if block + blocks > len(self.blocks):
            self.expand(block - len(self.blocks))
        self.blocks = (
            (self.blocks[:block] if block > 0 else [])
            + [id_] * blocks
            + self.blocks[block + blocks :]
        )


if __name__ == "__main__":
    d = Disk()

    last_id = d.load_raw(Path(sys.argv[1]).read_text(encoding="utf-8").strip())

    # move around data
    for id_ in range(last_id, 0, -1):
        blocks = d.scan_size(id_)
        if blocks is None:
            continue
        block = d.find_empty_block(blocks, d.scan_location(id_))
        if block:
            d.load_fragmented(id_)
            d.write_at(id_, block, blocks)

    # output
    # print("".join(map(lambda x: "." if x is None else str(x), d.blocks)))
    print(d.checksum())
