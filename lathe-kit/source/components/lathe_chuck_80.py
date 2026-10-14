"""Bought 80 mm 3-jaw self-centring scroll chuck, front mount (DIN 6350 style): envelope for fit and look.

Catalogue figures shared by several makers (Paulimot, Soba/Chronos, Indexa, Bison 3274-80): body Ø80 x 50 deep,
Ø55 recess in the back, 3 x M6 from the front on PCD 66, through bore about 16, clamping 2-70 mm, 4000 rpm
max, about 1.9 kg. Modelled in the actuator's frame (axis Z), seated on the backplate face (z 77.5); jaws shown
closed to Ø20. Not a made part: check the recess, bolt circle and screw length of the chuck actually bought.
"""
import math

import cadquery as cq
from steve import Component

z0, length = 77.5, 50.0  # mm back face (on the backplate), body length
front = z0 + length


def zcyl(r, h, z, x=0.0, y=0.0):
    return cq.Solid.makeCylinder(r, h, cq.Vector(x, y, z), cq.Vector(0, 0, 1))


body = zcyl(40, length, z0).cut(zcyl(27.5, 3, z0)).cut(zcyl(8, length, z0))
for k in range(3):
    a = math.radians(120 * k)                        # 3 x M6 from the front: Ø6.6 through, Ø11 x 6.5 counterbore
    x, y = 33 * math.cos(a), 33 * math.sin(a)
    body = body.cut(zcyl(3.3, length, z0, x, y)).cut(zcyl(5.5, 6.5, front - 6.5, x, y))
    b = math.radians(120 * k + 30)                   # chuck-key socket in the side
    body = body.cut(cq.Solid.makeCylinder(3.2, 14, cq.Vector(40 * math.cos(b), 40 * math.sin(b), z0 + 16),
                                          cq.Vector(-math.cos(b), -math.sin(b), 0)))
    slot = cq.Solid.makeBox(32, 10.4, 6, cq.Vector(8, -5.2, front - 6)).rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 120 * k + 60)
    body = body.cut(slot)                            # jaw guide slot, 10 wide, 6 deep

jaws = None
for k in range(3):                                   # stepped hard jaws, closed on Ø20
    jaw = cq.Solid.makeBox(20, 10, 14, cq.Vector(10, -5, front - 6))
    jaw = jaw.fuse(cq.Solid.makeBox(15, 10, 6, cq.Vector(15, -5, front + 8)))
    jaw = jaw.fuse(cq.Solid.makeBox(10, 10, 6, cq.Vector(20, -5, front + 14)))
    jaw = jaw.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 120 * k + 60)
    jaws = jaw if jaws is None else jaws.fuse(jaw)

lathe_chuck_80 = Component("lathe_chuck_80", name="3-jaw scroll chuck 80 mm, front mount (bought)")
lathe_chuck_80.add("body", body.clean(), name="Chuck body")
lathe_chuck_80.add("jaws", jaws.clean(), name="Jaws")
lathe_chuck_80.material("steel-s235jr", color="#3c3f45")   # cast-iron body and hardened jaws
