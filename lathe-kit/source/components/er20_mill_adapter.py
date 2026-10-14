"""ER20 milling adapter (branch "milling"), AISI 303: bolts to the actuator's output disk like the chuck
backplate (6 x M4 x 12 into the load holes, Ø20 pilot over the output hub) and carries an ER20 collet nose
(M25 x 1.5, 8° taper) with its nut. ER20 collets hold 1-13 mm cutters. Modelled in the actuator's frame
(axis Z, output face at z 65.5), placed with the mill's turn so the spindle points down. Collet and nut
shown as one with the body; the collet is closed on a Ø6 shank."""
import math

import cadquery as cq
from steve import Component


def zcyl(r, z0, z1):
    return cq.Solid.makeCylinder(r, z1 - z0, cq.Vector(0, 0, z0), cq.Vector(0, 0, 1))


body = zcyl(40, 65.5, 77.5).cut(zcyl(40.5, 65.5, 67.5).cut(zcyl(34, 65.5, 67.5)))
body = body.cut(zcyl(10, 65.5, 72.3))                # Ø20 H7 pilot over the output hub
for k in range(6):
    a = math.radians(60 * k + 30)
    x, y = 25 * math.cos(a), 25 * math.sin(a)
    body = body.cut(cq.Solid.makeCylinder(2.25, 12, cq.Vector(x, y, 65.5), cq.Vector(0, 0, 1)))
    body = body.cut(cq.Solid.makeCylinder(4.0, 4.5, cq.Vector(x, y, 73), cq.Vector(0, 0, 1)))
nose = zcyl(16, 77.5, 97)
nut = zcyl(17.5, 97, 115).cut(zcyl(10, 113, 115))
for k in range(6):                                   # spanner flats on the ER20 nut
    nut = nut.cut(cq.Solid.makeBox(4, 6, 10, cq.Vector(16.2, -3, 101)).rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 60 * k))
adapter = body.fuse(nose).fuse(nut).cut(zcyl(3.05, 80, 116))
er20_mill_adapter = Component("er20_mill_adapter", name="ER20 milling adapter (303)")
er20_mill_adapter.add("adapter", adapter.clean(), name="ER20 adapter")
er20_mill_adapter.material("stainless-304", finish="machined")
