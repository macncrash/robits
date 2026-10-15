"""Readhead standoff (made, 303), modelled at the origin along -Z: placed 4 x on the end bell's rear face at R24.5.

Ø4 x 7.38 body (end bell rear face z -48 to the readhead mounting surface z -55.38) with an M2 x 4 stud that
screws into the end bell and an M2 tapped hole (5 deep) for the readhead screw. Length sets the 2.88 ±0.13 ring-to-
readhead gap: make it 7.38 -0.02/-0.05 and shim the rest with RLS MB-ACC shims. CNC notes: build-pack/cnc/standoff.md.
"""
from steve import Component
from shapes import cyl, edge_break

standoff = Component("standoff", name="Readhead standoff")
body = cyl(2, 7.38, -7.38).fuse(cyl(1, 4, 0)).cut(cyl(0.8, 5, -7.38))
for r, z, size, out, up in ((2, 0, 0.2, -1, -1), (2, -7.38, 0.2, -1, 1)):
    body = body.cut(edge_break(r, z, size, out, up))
standoff.add("post", body.clean(), name="Standoff")
standoff.material("stainless-304", finish="machined")   # specified AISI 303; 304 stand-in
