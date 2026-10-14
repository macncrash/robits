"""Miter gauge: steel bar in the table's slot, 6061 protractor head engraved every degree +-60 (long every 5,
longer every 15) with a centre index, and a fence square to the disc at the 0 setting. Modelled at 0 degrees,
centred on x 0."""
import math

import cadquery as cq
from steve import Component
from sander_shapes import box, zcyl
from sander_params import table_y, table_z

slot_y = table_y - 60
bar = box(-60, slot_y - 9.45, table_z - 9.4, 60, slot_y + 9.45, table_z)
head = zcyl(45, table_z, table_z + 8, 0, slot_y).cut(box(-46, slot_y, table_z - 1, 46, slot_y + 46, table_z + 9))
for k in range(-60, 61):                             # scale on the curved edge's top face
    length = 7 if k % 15 == 0 else (5 if k % 5 == 0 else 3)
    a = math.radians(-90 + k)
    line = box(45 - length, -0.2, table_z + 7.6, 46, 0.2, table_z + 8.1)
    line = line.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), math.degrees(a)).translate(cq.Vector(0, slot_y, 0))
    head = head.cut(line)
fence = box(-3, slot_y - 70, table_z, 3, slot_y + 48, table_z + 30)
knob = zcyl(9, table_z + 8, table_z + 22, 0, slot_y - 30)
gauge = bar.fuse(head).fuse(fence).fuse(knob)
miter_gauge = Component("miter_gauge", name="Miter gauge")
miter_gauge.add("gauge", gauge.clean(), name="Miter gauge")
miter_gauge.material("aluminum-6061-t6", finish="brushed", color="#c9ccd1")
