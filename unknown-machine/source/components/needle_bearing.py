"""Needle bearing HK1210 pressed in the carrier: pilots the motor shaft's front end."""
import math

import cadquery as cq
from steve import Component
from shapes import ring, cyl

needle_bearing = Component("needle_bearing", name="Pilot needle bearing HK1210")
needle_bearing.add("shell", ring(9, 8.4, 10, 37), name="Drawn cup")
needles = [cyl(1.05, 9, 37.5, 7.3 * math.cos(2 * math.pi * k / 18), 7.3 * math.sin(2 * math.pi * k / 18)) for k in range(18)]
needle_bearing.add("needles", cq.Compound.makeCompound(needles), op="new", name="Needles")
needle_bearing.material("steel-1c60", finish="polished")
