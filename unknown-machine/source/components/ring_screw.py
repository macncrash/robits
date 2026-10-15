"""ISO 7046 M2 x 6 flat (countersunk) head screw, A2 (bought), modelled at catalogue size: head Ø3.8 x 90 deg,
origin on the head's top face, shank along +Z. Holds the encoder ring to its hub (8 x)."""
import cadquery as cq
from steve import Component

ring_screw = Component("ring_screw", name="ISO 7046 M2 x 6 countersunk screw (A2)")
head = cq.Solid.makeCone(1.9, 1.0, 0.9, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))
screw = head.fuse(cq.Solid.makeCylinder(1.0, 5.1, cq.Vector(0, 0, 0.9)))
ring_screw.add("screw", screw.clean(), name="Screw")
ring_screw.material("stainless-304", finish="polished")
