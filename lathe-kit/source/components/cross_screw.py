"""Cross-slide screw: SFU1204 ball screw (4 mm lead) under the cross-slide, along Y. It turns in the slide's
front bracket (Ø10 journal, thrust washers either side) and moves with the slide; its nut is fixed in the
carriage's block behind the slide, so the screw's tail shows behind the carriage as the slide comes forward."""
import cadquery as cq
from steve import Component
from lathe_shapes import ball_screw
from lathe_params import carriage_x

xc = carriage_x + 35
cross_screw = Component("cross_screw", name="Cross-slide screw SFU1204 ball screw")
screw = ball_screw(-94, 86, journals=((-121, -94),))
screw = screw.rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), -90).translate(cq.Vector(xc, 0, -75.2))
cross_screw.add("screw", screw, name="Cross screw")
cross_screw.material("steel-1c60", finish="machined")
