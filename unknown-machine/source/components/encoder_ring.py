"""RLS AksIM-2 ring MRA039BC020DSE00 (bought), at datasheet dimensions (MBD01_15).

Ø39 OD, Ø20 H7 bore, 2.0 thick: AISI 430 plate (mounting face, z -52.5, against the hub flange) and the rubber
magnet layer (magnetic face, z -54.5, toward the readhead). 8 countersunk holes for ISO 7046 M2 on PCD 25. The
plate / magnet split is approximate: take it from RLS's STEP model.
"""
import math

import cadquery as cq
from steve import Component
from shapes import ring

encoder_ring = Component("encoder_ring", name="Encoder ring RLS MRA039BC020DSE00")
holes = []
for k in range(8):
    a = math.radians(22.5 + 45 * k)
    x, y = 12.5 * math.cos(a), 12.5 * math.sin(a)
    holes.append(cq.Solid.makeCylinder(1.1, 3, cq.Vector(x, y, -55)))
    holes.append(cq.Solid.makeCone(1.9, 1.1, 0.8, cq.Vector(x, y, -54.5), cq.Vector(0, 0, 1)))   # 90 deg countersink
plate, magnet = ring(19.5, 10, 0.8, -53.3), ring(19.5, 10, 1.2, -54.5)
for h in holes:
    plate, magnet = plate.cut(h), magnet.cut(h)
encoder_ring.add("plate", plate, name="Steel plate")
encoder_ring.add("magnet", magnet, op="new", name="Magnet layer")
encoder_ring.material("steel-1c45", bodies=["plate"], color="#9aa0a6")   # AISI 430 stand-in
encoder_ring.material("tpu-98a", bodies=["magnet"], color="#3a3a3a")      # bonded ferrite in elastomer stand-in
