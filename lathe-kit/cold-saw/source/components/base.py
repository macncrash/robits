"""Base, 6061 plate on the stand top: the turntable sits in the middle on the plate (z 20); raised pads (z 30) in
front and at the sides carry the fence, the vise and the stock; the mitre scale ring is engraved -45..+45 degrees
(a line every degree, long every 5, longer every 15) and read by the turntable's pointer. The vise screw block
and the length-stop bracket are part of it."""
from steve import Component
from coldsaw_shapes import box, zcyl, sector_z
from coldsaw_params import table_z
import cadquery as cq

plate = box(-260, -220, 0, 260, 180, 20)
pads = box(-260, -220, 20, 260, -150, table_z)                       # front strip
for x0, x1 in ((-260, -200), (200, 260)):                           # side strips, clear of the swinging arm
    pads = pads.fuse(box(x0, -150, 20, x1, 25, table_z))
ring = sector_z(142, 170, -50, 50, 20, table_z)                     # mitre scale
for k in range(-45, 46):
    length = 12 if k % 15 == 0 else (8 if k % 5 == 0 else 4)
    line = box(-0.2, -170.5, table_z - 0.4, 0.2, -170 + length, table_z + 1)
    ring = ring.cut(line.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), k))
block = box(-145, -215, table_z, -125, -200, 60).cut(cq.Solid.makeCylinder(6.1, 20, cq.Vector(-135, -216, 38),
                                                                          cq.Vector(0, 1, 0)))
bracket = box(245, 30, 20, 260, 50, 75).cut(cq.Solid.makeCylinder(8.05, 20, cq.Vector(244, 40, 62),
                                                                    cq.Vector(1, 0, 0)))
base = plate.fuse(pads).fuse(ring).fuse(block).fuse(bracket)
base = base.cut(zcyl(141, 20, table_z + 1))                         # turntable pocket in the pads
base_c = Component("base", name="Base and mitre scale")
base_c.add("base", base.clean(), name="Base")
base_c.material("aluminum-6061-t6", finish="anodized", color="#15171c")
