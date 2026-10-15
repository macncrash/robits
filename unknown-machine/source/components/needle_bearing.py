"""Needle bearing HK1210 (12 x 16 x 10, drawn cup) pressed in the carrier: pilots the motor shaft's front end.
The needles run straight on the shaft (hardened, ground journal z 37..47)."""
import math

import cadquery as cq
from steve import Component
from shapes import ring, cyl

needle_bearing = Component("needle_bearing", name="Pilot needle bearing HK1210")
needle_bearing.add("shell", ring(8, 7.5, 10, 37), name="Drawn cup")
needles = [cyl(0.7, 9, 37.5, 6.75 * math.cos(2 * math.pi * k / 24), 6.75 * math.sin(2 * math.pi * k / 24)) for k in range(24)]
needle_bearing.add("needles", cq.Compound.makeCompound(needles), op="new", name="Needles")
needle_bearing.material("steel-1c60", finish="polished")
