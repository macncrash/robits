"""Motor can: rear section, finned stator section, front section and bulkhead with the crossed-roller output-bearing seat."""
import math

from steve import Component
from shapes import ring, cyl, ycyl
from assembly_data import SCREW_PCD, SCREW_ANGLES

housing = Component("housing", name="Motor housing")

stator_bore = 42.55                                  # radius: KBM-17 stator 84.963 + 0.07 mm slip fit per side, bonded
shell = ring(51.5, stator_bore, 10, -36)             # rear section, z -36..-26 (stator goes in from the rear)
fins = ring(48, stator_bore, 40, -26)                # finned section, z -26..14
for k in range(1, 9):
    fins = fins.cut(ring(48.1, 45, 2.5, -26 + 40 * k / 9 - 1.25))
front = ring(56, stator_bore, 15, 14)                # front section, z 14..29 (clamp band sits on z 20..32)
front = front.fuse(ring(56, 40.5, 2, 29))            # depth-stop ledge z 29..31: the stator sleeve banks against it
bulkhead = ring(56, 24, 13, 31).cut(cyl(30, 10, 34))   # z 31..44, CRBH 3510 crossed-roller seat (60 mm) open to the front
body = shell.fuse(fins).fuse(front).fuse(bulkhead)
for a in SCREW_ANGLES:                               # M5 tapped holes (tap drill 4.2) for the flange screws
    r = SCREW_PCD / 2
    body = body.cut(cyl(2.1, 12, 32, r * math.cos(math.radians(a)), r * math.sin(math.radians(a))))
for z in (29, 39):                                   # M5 tapped (4.2 drill) for the 4 pedestal screws, ~10 mm of thread
    for x in (-16, 16):
        body = body.cut(ycyl(2.1, -58, -42.5, x, z))
for z in (22, 40):                                   # 4 mm holes for the two locating dowels, 6 deep
    body = body.cut(ycyl(2, -58, -50, 0, z))
housing.add("shell", body.clean(), name="Housing")
housing.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
