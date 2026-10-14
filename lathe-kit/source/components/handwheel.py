"""Handwheel with graduated dial (all four slides use the same one): steel hub, satin-aluminium dial ring with
100 engraved lines (0.02 mm each on a 2 mm-pitch screw, a long line every 10), 70 mm wheel with a crank handle.
Built along +Z from its mounting face at the origin; each instance is turned onto its screw's axis."""
from steve import Component
from lathe_shapes import zcyl, box, ring_marks
import cadquery as cq

hub = zcyl(8, 0, 2)
dial = zcyl(20, 2, 14).cut(ring_marks(20, 2, 100, 10, 3.0, 5.5))
wheel = zcyl(35, 14, 20)
for k in range(3):                                   # lightening holes
    a = 120 * k + 60
    wheel = wheel.cut(zcyl(8, 14, 20, 22 * cq.Vector(1, 0, 0).x, 0).rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a))
crank = zcyl(4, 20, 38, 27, 0).fuse(zcyl(6.5, 38, 52, 27, 0))
wheel_all = hub.fuse(dial).fuse(wheel).fuse(crank).cut(zcyl(5, -1, 21))
handwheel = Component("handwheel", name="Handwheel with 100-line dial")
handwheel.add("handwheel", wheel_all.clean(), name="Handwheel")
handwheel.material("aluminum-6061-t6", finish="brushed", color="#c9ccd1")
