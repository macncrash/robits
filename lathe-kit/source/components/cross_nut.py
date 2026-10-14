"""Cross-slide ball nut: SFU1204 flanged nut through the carriage's nut block behind the slide, flange on the
block's back face (4 x M4), flat down into a recess in the carriage top."""
import cadquery as cq
from steve import Component
from lathe_shapes import ball_nut
from lathe_params import carriage_x

xc = carriage_x + 35
nut = ball_nut().rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), -90).translate(cq.Vector(xc, -8, -75.2))
cross_nut = Component("cross_nut", name="Cross-slide ball nut SFU1204 (bought)")
cross_nut.add("nut", nut, name="Ball nut")
cross_nut.material("steel-1c60", finish="machined", color="#4a4d52")
