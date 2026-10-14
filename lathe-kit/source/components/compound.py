"""Compound swivel base: turns on the cross-slide (one M8 pivot, two clamp nuts) and carries the top-slide
dovetail. Its rim is engraved +-60 degrees, a line every degree and a long one every 10, read against the zero
mark on the cross-slide, for cutting tapers and chamfers.
"""
from steve import Component
from lathe_shapes import zcyl, box, prism_yz, xcyl, ring_marks
from lathe_params import carriage_x, tool_y

xc = carriage_x + 35
base = zcyl(30, -56, -48, xc, tool_y)
marks = ring_marks(30, -51, 120, 10, 2.0, 3.5, span=120, start=-90 - 60)   # +-60 deg about the -Y (front) side
base = base.cut(marks.translate((xc, tool_y, 0)))
dovetail = [(tool_y - 12, -48), (tool_y + 12, -48), (tool_y + 15, -38), (tool_y - 15, -38)]   # top-slide ways along X
base = base.fuse(prism_yz(dovetail, xc - 40, xc + 40))
base = base.cut(xcyl(5.5, xc - 41, xc + 41, tool_y, -43.2))   # slot for the top-slide screw
compound = Component("compound", name="Compound swivel base")
compound.add("compound", base.clean(), name="Swivel base")
compound.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
