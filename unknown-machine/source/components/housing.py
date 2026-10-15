"""Motor can: rear section, finned stator section, front section and bulkhead with the crossed-roller output-bearing seat.

Made by turning (rear op: stator bore, adhesive grooves, fins; front op: Ø120, Ø60 bearing seat, Ø90 flange
counterbore for the bearing clamp ring) then milling the axial, radial and rear-face holes. CNC notes: build-pack/cnc/housing.md.
"""
import math

from steve import Component
from shapes import ring, cyl, ycyl, edge_break, drill_point
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
bulkhead = ring(front_r, 24, 13, 31).cut(cyl(30, 10, 32.5))   # z 31..44, CRBH 3510 crossed-roller seat (60 mm) z 32.5..42.5
body = shell.fuse(fins).fuse(front).fuse(bulkhead)
body = body.cut(cyl(45, 2, 42.4))                    # Ø90 H7 counterbore 1.6 deep: the bearing clamp ring sits in it and centres the
                                                     # front flange (and ring gear); 0.1 below the bearing so the clamp bears on the bearing
for k in range(6):                                   # adhesive grooves for the bonded stator (Kollmorgen: 0.13-0.26 deep over
    body = body.cut(ring(stator_bore + 0.2, 42.4, 5, -26 + 9 * k))   # half the bore): 6 x 5 wide, 0.2 deep, z -26..24
body = body.cut(ring(30.3, 29.6, 1.1, 32.2))         # corner relief 0.3 x 0.3 under the CRBH outer ring (seat floor z 32.5)
body = body.cut(ring(42.85, 42.25, 0.6, 28.7))       # corner relief 0.3 x 0.3 where the stator banks on the ledge (z 29)
for r, z, size, out, up in ((stator_bore, -36, 0.5, 1, 1),   # lead-in: stator / end-bell spigot entry
                            (30, 42.4, 0.5, 1, -1),          # lead-in: CRBH seat entry
                            (front_r, 44, 0.5, -1, -1),      # front face OD
                            (front_r, 14, 0.5, -1, 1),       # Ø120 / Ø96 step (clears the saddle's corner)
                            (51.5, -36, 0.5, -1, 1)):        # rear face OD
    body = body.cut(edge_break(r, z, size, out, up))
for a in SCREW_ANGLES:                               # M5 tapped (4.2 drill) z 26..44 for the M5 x 30 flange screws:
    r = SCREW_PCD / 2                                # 14.5 mm of thread (2.9 d), 3.5 mm below the tip, 7.9 mm wall to the OD
    x, y = r * math.cos(math.radians(a)), r * math.sin(math.radians(a))
    body = body.cut(cyl(2.1, 18, 26, x, y)).cut(drill_point(2.1, (x, y, 26), (0, 0, -1)))
for z in (28, 37):                                   # M5 tapped (4.2 drill) to y -43.5 for the 4 pedestal screws: surface
    for x in (-16, 16):                              # at y -57.8, ~11 mm of thread, 2.5 mm below the tip, 4.1 mm to the stator bore
        body = body.cut(ycyl(2.1, -60, -43.5, x, z)).cut(drill_point(2.1, (x, -43.5, z), (0, 1, 0)))
for k in range(4):                                   # M4 tapped (3.3 drill, 10.5 deep) in the rear face, PCD 92, for the end-bell
    a = math.radians(45 + 90 * k)                    # screws (ISO 4762 M4 x 16: 8.5 mm of thread)
    x, y = 46 * math.cos(a), 46 * math.sin(a)
    body = body.cut(cyl(1.65, 10.5, -36, x, y)).cut(drill_point(1.65, (x, y, -25.5), (0, 0, 1)))
for z in (22, 40):                                   # 4 mm holes for the two locating dowels, 8 deep (dowel in 6)
    body = body.cut(ycyl(2, -60, -52, 0, z)).cut(drill_point(2, (0, -52, z), (0, 1, 0)))
housing.add("shell", body.clean(), name="Housing")
housing.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
