"""Clamp ring for the CRBH 3510 outer ring (made, 303).

Sits in the housing's Ø90 H7 counterbore and in the front flange's Ø90 H7 recess, so it also centres the flange
(and the ring gear) on the bearing axis. Its inner lip (r 27..34, 1.0 thick) bears on the outer ring's front face;
the flange screws clamp it. It is captive between the carrier plate and the bearing, so it goes in and out with
the carrier. CNC notes: build-pack/cnc/bearing_clamp.md.
"""
import cadquery as cq
from steve import Component
from shapes import edge_break

bearing_clamp = Component("bearing_clamp", name="Output bearing clamp ring")
profile = [(27, 42.5), (45, 42.5), (45, 45), (34, 45), (34, 43.5), (27, 43.5)]
clamp = cq.Workplane("XZ").polyline(profile).close().revolve(360, (0, 0, 0), (0, 1, 0)).val()
for r, z, size, out, up in ((45, 42.5, 0.3, -1, 1), (45, 45, 0.3, -1, -1), (27, 42.5, 0.2, 1, 1), (27, 43.5, 0.2, 1, -1),
                            (34, 45, 0.3, 1, -1)):
    clamp = clamp.cut(edge_break(r, z, size, out, up))
bearing_clamp.add("clamp", clamp, name="Clamp ring")
bearing_clamp.material("stainless-304", finish="machined")   # specified AISI 303 (1.4305); 304 stand-in
