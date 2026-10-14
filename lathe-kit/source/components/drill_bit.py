"""6 mm HSS jobber drill in the ER16 collet chuck (118 degree point)."""
import math

import cadquery as cq
from steve import Component
from lathe_shapes import xcyl
from lathe_params import tailstock_x

x_nose = tailstock_x - 30
tip = 210.0
point = 3 / math.tan(math.radians(59))
drill = cq.Solid.makeCone(0.01, 3, point, cq.Vector(tip, 0, 0), cq.Vector(1, 0, 0)).fuse(xcyl(3, tip + point, x_nose - 8))
drill_bit = Component("drill_bit", name="Drill 6 mm HSS")
drill_bit.add("drill", drill.clean(), name="Drill")
drill_bit.material("steel-1c60", color="#4a4d52")
