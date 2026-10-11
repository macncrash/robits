"""Front flange: holds the ring gear, bolts to the housing with four M5 socket-head screws."""
import math

from steve import Component
from shapes import cyl, ring
from assembly_data import SCREW_PCD, SCREW_ANGLES

front_flange = Component("front_flange", name="Front flange")
body = ring(60, 39, 4, 44).fuse(ring(60, 43, 17, 48))
for a in SCREW_ANGLES:
    x, y = SCREW_PCD / 2 * math.cos(math.radians(a)), SCREW_PCD / 2 * math.sin(math.radians(a))
    body = body.cut(cyl(2.75, 22, 43.5, x, y)).cut(cyl(4.75, 6, 59.5, x, y))
front_flange.add("flange", body.clean(), name="Flange")
front_flange.material("aluminum-6061-t6", finish="anodized", color="#22283a")
