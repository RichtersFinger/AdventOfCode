"""Advent of Code 2024 - Day 6: Guard Gallivant (Part 2)"""

import sys
from pathlib import Path

import common


# find baseline, only the timeline0-path is relevant for placing obstacle
raw_input = Path(sys.argv[1]).read_text(encoding="utf-8")
_, timeline0 = common.Simulation(raw_input).run()

# iterate timelines
good_timelines = []
for target in timeline0:
    alternative_timeline = common.Simulation(raw_input)
    if target == (
        alternative_timeline.guard.p.x,
        alternative_timeline.guard.p.y,
    ):
        continue
    alternative_timeline.alter(common.Vector(target[0], target[1]), "#")
    trapped, _ = alternative_timeline.run()
    if trapped:
        good_timelines.append(target)


print(good_timelines)
print("---------")
print("= ", len(good_timelines))
