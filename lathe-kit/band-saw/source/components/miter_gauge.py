"""Miter gauge: steel bar in the table's slot, 6061 protractor head engraved every degree +-60 (long every 5,
longer every 15), and a fence square to the blade at 0, stopping 10 mm short of it. Modelled at 0 degrees, in
front of the blade."""
import math

import cadquery as cq
from steve import Component
from bandsaw_shapes import box, zcyl

sx, hy = -90, -80
bar = box(sx - 9.45, -140, -9.4, sx + 9.45, 20, 0)
head = zcyl(45, 0, 8, sx, hy).cut(box(sx - 46, hy, -1, sx + 46, hy + 46, 9))
for k in range(-60, 61):
    length = 7 if k % 15 == 0 else (5 if k % 5 == 0 else 3)
    line = box(45 - length, -0.2, 7.6, 46, 0.2, 8.1)
    line = line.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), -90 + k).translate(cq.Vector(sx, hy, 0))
    head = head.cut(line)
fence = box(sx - 40, hy, 0, -10, hy + 6, 30)
knob = zcyl(9, 8, 22, sx, hy - 30)
miter_gauge = Component("miter_gauge", name="Miter gauge")
miter_gauge.add("gauge", bar.fuse(head).fuse(fence).fuse(knob).clean(), name="Miter gauge")
miter_gauge.material("aluminum-6061-t6", finish="brushed", color="#c9ccd1")
