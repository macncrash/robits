"""Pedestal: saddle that cradles the clamp band, side cable port, square base plate with four holes."""
import cadquery as cq
from steve import Component
from shapes import box, cyl

pedestal = Component("pedestal", name="Pedestal")
block = box(-40, -78, 0, 40, -30, 44).cut(cyl(60.2, 50, -3))
block = block.cut(box(-41, -74, 10, 41, -66, 24))                       # side cable port
plate = (cq.Workplane("XZ", origin=(0, -78, 0)).center(0, 22).rect(130, 100).extrude(10)
         .edges("|Y").fillet(10).val())
for x, z in ((-52, -15), (52, -15), (-52, 59), (52, 59)):
    plate = plate.cut(cq.Solid.makeCylinder(4.5, 12, cq.Vector(x, -77, z), cq.Vector(0, -1, 0)))
pedestal.add("body", block.fuse(plate).clean(), name="Pedestal")
pedestal.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
