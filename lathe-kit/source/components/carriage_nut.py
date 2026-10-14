"""Carriage ball nut: SFU1204 flanged nut in the carriage's nut housing, flange on the housing's right-hand
face (4 x M4), the catalogue flat toward the bed. Buy it preloaded (oversize balls or a DFU double nut) so the
dial has no backlash to take up."""
import cadquery as cq
from steve import Component
from lathe_shapes import ball_nut
from lathe_params import carriage_x

xc = carriage_x + 35
nut = ball_nut().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90).translate(cq.Vector(xc - 10, -67.5, -120))
carriage_nut = Component("carriage_nut", name="Carriage ball nut SFU1204 (bought)")
carriage_nut.add("nut", nut, name="Ball nut")
carriage_nut.material("steel-1c60", finish="machined", color="#4a4d52")
