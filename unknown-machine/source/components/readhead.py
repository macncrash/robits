"""RLS AksIM-2 readhead MB039DCC18BENT00 (bought), at datasheet dimensions (MBD01_15).

A 196 deg arc of PCB, R10.6..R27, 1.6 thick, sensor side facing forward to the ring. Its mounting surface (z -55.38)
is the ring mounting face (z -52.5) - 2.88: ride height 0.23 to the magnetic face. 4 x Ø2.2 holes on R24.5 at 0, 60,
120, 180 deg; components up to 5.2 above the mounting surface (on the rear side here; check the RLS STEP model).
The connector (FCI 10114830-11108LF, tangential) is not modelled.
"""
import math

import cadquery as cq
from steve import Component

z_mount = -55.38   # mounting surface (sensor side)


def sector(r_in, r_out, a0, a1, z0, h):
    """Annular sector a0..a1 degrees, z0..z0+h."""
    w = cq.Workplane("XY").workplane(offset=z0)
    outer = w.circle(r_out).extrude(h).val()
    s = outer.cut(cq.Solid.makeCylinder(r_in, h, cq.Vector(0, 0, z0)))
    wedge = cq.Workplane("XY").workplane(offset=z0).polyline(
        [(0, 0)] + [(40 * math.cos(math.radians(a0 + (a1 - a0) * i / 8)), 40 * math.sin(math.radians(a0 + (a1 - a0) * i / 8)))
                    for i in range(9)]).close().extrude(h).val()
    return s.intersect(wedge)


readhead = Component("readhead", name="Encoder readhead RLS MB039DCC18BENT00")
pcb = sector(10.6, 27, -8, 188, z_mount - 1.6, 1.6)
for k in range(4):
    a = math.radians(60 * k)
    pcb = pcb.cut(cq.Solid.makeCylinder(1.1, 3, cq.Vector(24.5 * math.cos(a), 24.5 * math.sin(a), z_mount - 2.5)))
readhead.add("pcb", pcb, name="PCB")
readhead.add("sensor", sector(14.5, 18.5, 66, 114, z_mount, 0.65), op="new", name="Sensor")
readhead.add("parts", sector(12, 22, 15, 165, z_mount - 5.2, 3.6), op="new", name="Components")
readhead.material("pc", color="#2a7d4f")
