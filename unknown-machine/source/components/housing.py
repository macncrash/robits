"""Motor can: rear section, finned stator section, front section and bulkhead with the crossed-roller output-bearing seat."""
import math

from steve import Component
from shapes import ring, cyl
from assembly_data import SCREW_PCD, SCREW_ANGLES

housing = Component("housing", name="Motor housing")

shell = ring(51.5, 42, 10, -36)                      # rear section, z -36..-26
fins = ring(48, 42, 40, -26)                         # finned section, z -26..14
for k in range(1, 9):
    fins = fins.cut(ring(48.1, 45, 2.5, -26 + 40 * k / 9 - 1.25))
front = ring(56, 42, 22, 14)                         # front section, z 14..36 (clamp band sits here)
bulkhead = ring(56, 24, 13, 31).cut(cyl(30, 10, 34))   # z 31..44, CRBH 3510 crossed-roller seat (60 mm) open to the front
body = shell.fuse(fins).fuse(front).fuse(bulkhead)
for a in SCREW_ANGLES:                               # M5 tapped holes (tap drill 4.2) for the flange screws
    r = SCREW_PCD / 2
    body = body.cut(cyl(2.1, 12, 32, r * math.cos(math.radians(a)), r * math.sin(math.radians(a))))
housing.add("shell", body.clean(), name="Housing")
housing.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
