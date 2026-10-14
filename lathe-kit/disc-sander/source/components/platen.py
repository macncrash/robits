"""Platen: Ø250 x 10 6061 disc, faced true on its own hub after assembly, 6 x M5 countersunk (flush under the
abrasive) into the hub on PCD 66. The PSA abrasive disc sticks to its front face."""
import math

import cadquery as cq
from steve import Component
from sander_shapes import ycyl
from sander_params import disc_d, disk_face, hub_t, platen_t

y_back = -disk_face - hub_t
y_front = y_back - platen_t
plate = ycyl(disc_d / 2, y_front, y_back).cut(ycyl(8, y_front, y_back))
for k in range(6):
    b = math.radians(60 * k)
    x, z = 33 * math.cos(b), 33 * math.sin(b)
    plate = plate.cut(ycyl(2.75, y_front, y_back, x, z))
    plate = plate.cut(cq.Solid.makeCone(5.2, 2.75, 2.45, cq.Vector(x, y_front, z), cq.Vector(0, 1, 0)))
platen = Component("platen", name="Platen Ø250 (6061)")
platen.add("platen", plate.clean(), name="Platen")
platen.material("aluminum-6061-t6", finish="machined")
