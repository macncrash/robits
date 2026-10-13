"""Drawn-cup needle bearing HK0609 (6 x 10 x 9) pressed in each planet; runs on the hardened planet pin.

Modelled at the origin like the planet (z 1.5..10.5, centred in the 12 mm face), placed 3x by main.py.
"""
import math

import cadquery as cq
from steve import Component
from shapes import ring, cyl

planet_needle = Component("planet_needle", name="Planet needle bearing HK0609")
planet_needle.add("shell", ring(5, 4.5, 9, 1.5), name="Drawn cup")
needles = [cyl(0.73, 8, 2, 3.76 * math.cos(2 * math.pi * k / 12), 3.76 * math.sin(2 * math.pi * k / 12)) for k in range(12)]
planet_needle.add("needles", cq.Compound.makeCompound(needles), op="new", name="Needles")
planet_needle.material("steel-1c60", finish="polished")
