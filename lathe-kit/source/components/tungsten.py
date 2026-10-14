"""TIG electrode, 2.4 x 75 (lanthanated or ceriated: grinding thoriated tungsten makes radioactive dust), ground
to a 30 degree point; in the holder, tip on the diamond disc."""
import math

import cadquery as cq
from steve import Component

half_angle, tip_y, tip_x, r = 15, -28, 159.05 + 20, 1.2
cone_len = r / math.tan(math.radians(half_angle))
rod = cq.Solid.makeCone(0.01, r, cone_len, cq.Vector(0, 0, 0), cq.Vector(0, 1, 0))
rod = rod.fuse(cq.Solid.makeCylinder(r, 75 - cone_len, cq.Vector(0, cone_len, 0), cq.Vector(0, 1, 0)))
rod = rod.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 180 + half_angle).translate(cq.Vector(tip_x, tip_y, 0))
tungsten = Component("tungsten", name="TIG tungsten 2.4 mm, 30 deg point")
tungsten.add("electrode", rod.clean(), name="Electrode")
tungsten.material("steel-1c60", color="#9a9ea6")   # tungsten is not in the library; appearance only
