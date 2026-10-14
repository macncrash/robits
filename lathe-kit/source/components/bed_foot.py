"""Bed foot: one at each end, bolted under the bed; slotted for bench bolts."""
from steve import Component
from lathe_shapes import box, zcyl

bed_foot = Component("bed_foot", name="Bed foot")
foot = box(0, -75, -163, 40, 75, -143)
for y in (-30, 30):
    foot = foot.cut(zcyl(4.5, -163, -143, 20, y))
for y in (-62, 62):                                  # bench bolt slots
    foot = foot.cut(zcyl(4.5, -163, -143, 14, y)).cut(zcyl(4.5, -163, -143, 26, y)).cut(box(14, y - 4.5, -163, 26, y + 4.5, -143))
bed_foot.add("foot", foot.clean(), name="Foot")
bed_foot.material("aluminum-6061-t6", finish="anodized", color="#15171c")
