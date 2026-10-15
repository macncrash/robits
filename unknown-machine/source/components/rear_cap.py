"""Knurled encoder cover on the back of the end bell, with the hollow-shaft cable exit.

The 48 grip flutes are slots 2 wide with round ends, cut radially with a Ø2 end mill on a C-axis lathe (or 4th
axis). Three bosses inside carry ISO 7380 M3 x 25 screws into the end bell (R1.5 where they meet the cavity wall,
milled with the cavity from the front); a Ø7 hole in the rear face (with a grommet) lets the encoder cable out. CNC notes: build-pack/cnc/rear_cap.md.
"""
import math

from steve import Component
from shapes import cyl, box, xcyl, turned, edge_break

rear_cap = Component("rear_cap", name="Encoder cap (knurled)")
cap = cyl(42, 17, -65).cut(cyl(39, 14, -62)).cut(cyl(5, 4, -66))
for k in range(3):                                      # screw bosses at R37 (clear of the readhead's R27 and its standoffs)
    a = math.radians(30 + 120 * k)
    cap = cap.fuse(cyl(3, 14, -62, 37 * math.cos(a), 37 * math.sin(a)))
    cap = cap.cut(cyl(1.7, 19, -66, 37 * math.cos(a), 37 * math.sin(a)))   # Ø3.4 clearance
cap = cap.fillet(1.5, [e for e in cap.Edges() if e.geomType() == "LINE" and abs(e.startPoint().x - e.endPoint().x) < 1e-6
                        and abs(e.startPoint().y - e.endPoint().y) < 1e-6 and abs(math.hypot(e.startPoint().x, e.startPoint().y) - 39) < 1e-3
                        and abs(e.startPoint().y) > 1e-3])   # boss-to-wall corners (not the cylinder's seam at +X)
flute = box(41.2, -1, -62.5, 43, 1, -51).fuse(xcyl(1, 41.2, 43, 0, -62.5)).fuse(xcyl(1, 41.2, 43, 0, -51))   # 1.5 from the rear face
for k in range(48):
    cap = cap.cut(turned(flute, 7.5 * k))
cap = cap.cut(cyl(3.5, 5, -66, 32 * math.cos(math.radians(-30)), 32 * math.sin(math.radians(-30))))   # Ø7 encoder cable exit
for z, up in ((-65, 1), (-48, -1)):                    # outer edge breaks
    cap = cap.cut(edge_break(42, z, 0.5, -1, up))
rear_cap.add("cap", cap.clean(), name="Cap")
rear_cap.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
