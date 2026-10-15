"""Front flange: holds the ring gear, bolts to the housing with four M5 socket-head screws.

A Ø90 H7 recess (1.0 deep) in its rear face fits over the bearing clamp ring, which also sits in the housing's
Ø90 H7 counterbore: the ring centres the flange, and with it the ring gear, on the output-bearing axis (the screws
alone, in Ø5.5 clearance holes, would let it float ±0.25 mm), and the flange presses the ring onto the CRBH outer
ring. Turned with the Ø86 ring-gear bore and the Ø90 recess in one op. CNC notes: build-pack/cnc/front_flange.md.
"""
import math

from steve import Component
from shapes import cyl, ring, edge_break
from assembly_data import SCREW_PCD, SCREW_ANGLES

front_flange = Component("front_flange", name="Front flange")
body = ring(60, 39, 4, 44).fuse(ring(60, 43, 17, 48)).cut(ring(45, 38.5, 1, 44))   # lip, ring-gear bore, Ø90 recess
body = body.cut(ring(43.3, 42.7, 1.1, 47.7))         # corner relief 0.3 x 0.3 where the ring gear seats (z 48)
for r, z, size, out, up in ((43, 65, 0.5, 1, -1),    # lead-in: ring-gear press fit
                            (60, 65, 0.5, -1, -1), (60, 44, 0.5, -1, 1),   # OD edges
                            (45, 44, 0.3, 1, 1),     # recess lead-in
                            (39, 48, 0.3, 1, -1)):   # lip bore edge
    body = body.cut(edge_break(r, z, size, out, up))
for a in SCREW_ANGLES:
    x, y = SCREW_PCD / 2 * math.cos(math.radians(a)), SCREW_PCD / 2 * math.sin(math.radians(a))
    body = body.cut(cyl(2.75, 22, 43.5, x, y)).cut(cyl(4.75, 6, 59.5, x, y))
front_flange.add("flange", body.clean(), name="Flange")
front_flange.material("aluminum-6061-t6", finish="anodized", color="#22283a")
