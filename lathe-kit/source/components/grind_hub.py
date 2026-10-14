"""Tungsten grinding hub: a steel arbor with a Ø20 shank gripped in the 3-jaw chuck, and a Ø75 plated-diamond disc
on its flange (one countersunk M6, flush), grinding face toward the tailstock. Ø75 keeps the disc clear of the top
slide when the tool post is brought up to it. At 1060 rpm the face runs about 4 m/s at its rim: slow by tungsten-
grinder standards (about 13 m/s), but diamond on tungsten doesn't need speed, only light feed.
"""
import cadquery as cq
from steve import Component
from lathe_shapes import xcyl

disc_face = 159.0                                     # grinding face (x)
arbor = xcyl(10, 129, 150).fuse(xcyl(25, 150, disc_face - 3))
disc = xcyl(37.5, disc_face - 3, disc_face)
screw_seat = cq.Solid.makeCone(3.3, 6.5, 3.2, cq.Vector(disc_face - 3.2, 0, 0), cq.Vector(1, 0, 0))
disc = disc.cut(screw_seat)
grind_hub = Component("grind_hub", name="Tungsten grinding hub, Ø75 diamond disc")
grind_hub.add("arbor", arbor.clean(), name="Arbor")
grind_hub.add("disc", disc.clean(), name="Diamond disc Ø75 (plated, D64-D91 grit)")
grind_hub.material("steel-1c45", finish="machined")
grind_hub.material("steel-1c45", bodies=["disc"], color="#7d8088")
