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
front_r = 60                                         # front section and bulkhead Ø120 (= flange OD): wall round the M5 threads
front = ring(front_r, stator_bore, 15, 14)           # front section, z 14..29 (sits in the pedestal saddle)
front = front.fuse(ring(front_r, 40.5, 2, 29))       # depth-stop ledge z 29..31: the stator sleeve banks against it
bulkhead = ring(front_r, 24, 13, 31).cut(cyl(30, 10, 34))   # z 31..44, CRBH 3510 crossed-roller seat (60 mm) open to the front
body = shell.fuse(fins).fuse(front).fuse(bulkhead)
for a in SCREW_ANGLES:                               # M5 tapped (4.2 drill) z 26..44 for the M5 x 30 flange screws:
    r = SCREW_PCD / 2                                # 14.5 mm of thread (2.9 d), 3.5 mm below the tip, 7.9 mm wall to the OD
    body = body.cut(cyl(2.1, 18, 26, r * math.cos(math.radians(a)), r * math.sin(math.radians(a))))
for z in (28, 37):                                   # M5 tapped (4.2 drill) to y -43.5 for the 4 pedestal screws: surface
    for x in (-16, 16):                              # at y -57.8, ~11 mm of thread, 2.5 mm below the tip, 4.1 mm to the stator bore
        body = body.cut(ycyl(2.1, -60, -43.5, x, z))
for z in (22, 40):                                   # 4 mm holes for the two locating dowels, 8 deep (dowel in 6)
    body = body.cut(ycyl(2, -60, -52, 0, z))
housing.add("shell", body.clean(), name="Housing")
housing.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
