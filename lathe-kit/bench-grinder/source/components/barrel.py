"""Motor barrel: 6061 tube, the stator bonded in its Ø85 bore. 4 x M5 tapped in each end for the end bells,
2 x M6 underneath into the head foot, and a Ø14 port underneath for the motor and sensor cables, which run down
inside the column to the drive box."""
import math
from steve import Component
from grinder_shapes import xring, xcyl, zcyl
from grinder_params import spindle_z

body = xring(54, 42.5, -40, 40)
for s in (1, -1):
    for a in (45, 135, 225, 315):
        y, z = 48 * math.cos(math.radians(a)), spindle_z + 48 * math.sin(math.radians(a))
        x0 = 28 if s > 0 else -41
        body = body.cut(xcyl(2.1, x0, x0 + 13, y, z))
for x in (-20, 20):
    body = body.cut(zcyl(2.5, spindle_z - 55, spindle_z - 45, x, 0))
body = body.cut(zcyl(7, spindle_z - 55, spindle_z - 40, 0, 0))
barrel = Component("barrel", name="Motor barrel")
barrel.add("barrel", body.clean(), name="Barrel")
barrel.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
