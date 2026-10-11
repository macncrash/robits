"""ISO 4762 M5 x 25 socket head cap screw (head on top, modelled at the origin)."""
import cadquery as cq
from steve import Component
from shapes import cyl

flange_screw = Component("flange_screw", name="M5x25 socket head screw")
socket = cq.Workplane("XY").workplane(offset=2).polygon(6, 4.6).extrude(3.1).val()
screw = cyl(2.5, 25, -25).fuse(cyl(4.25, 5, 0)).cut(socket)
flange_screw.add("screw", screw.clean(), name="Screw")
flange_screw.material("stainless-304", finish="brushed")
