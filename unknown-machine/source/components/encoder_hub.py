"""Encoder hub (made, 303): carries the RLS MRA039 ring on the shaft's rear end.

Ø12 H7 bore on the shaft (Loctite 638 plus one M2 set screw in the flange), Ø30 x 4 flange with 8 x M2 tapped through
holes on PCD 25 for the ring's ISO 7046 M2 x 6 screws, Ø20 g6 pilot 1.8 long for the ring's Ø20 H7 bore (RLS
recommends g6). Behind the ring it stays under Ø21.2 (the readhead's bore): collar Ø18 to z -58.
Stack (design z): flange z -48.5..-52.5 (0.5 clear of the end bell), ring mounting face -52.5. CNC notes:
build-pack/cnc/encoder_hub.md.
"""
import math

import cadquery as cq
from steve import Component
from shapes import cyl, xcyl, edge_break

encoder_hub = Component("encoder_hub", name="Encoder hub")
profile = [(6, -48.5), (15, -48.5), (15, -52.5), (10, -52.5), (10, -54.3), (9, -54.3), (9, -58), (6, -58)]
hub = cq.Workplane("XZ").polyline(profile).close().revolve(360, (0, 0, 0), (0, 1, 0)).val()
for k in range(8):                                   # M2 tapped through the flange (1.6 drill)
    a = math.radians(22.5 + 45 * k)
    hub = hub.cut(cyl(0.8, 5, -53, 12.5 * math.cos(a), 12.5 * math.sin(a)))
hub = hub.cut(xcyl(0.8, 5.5, 16, 0, -50.5))           # M2 set screw (1.6 drill) radially through the flange, between the ring screws
for r, z, size, out, up in ((15, -48.5, 0.3, -1, -1), (15, -52.5, 0.3, -1, 1), (10, -54.3, 0.3, -1, 1),
                            (9, -58, 0.3, -1, 1), (6, -48.5, 0.3, 1, -1), (6, -58, 0.3, 1, 1)):
    hub = hub.cut(edge_break(r, z, size, out, up))
encoder_hub.add("hub", hub, name="Hub")
encoder_hub.material("stainless-304", finish="machined")   # specified AISI 303 (1.4305); 304 stand-in
