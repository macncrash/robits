"""Mitre turntable, 6061: a Ø280 disc on the base, turning about the point where the blade meets the fence, with
the blade slot, the front pointer for the degree scale, and the arm out to the chop-pivot cheeks at the back.
The head swings with it 45 degrees either way; a lock lever (not modelled) clamps it, with detents at 0 and 45."""
from steve import Component
from coldsaw_shapes import box, zcyl, xcyl
from coldsaw_params import table_z, pivot_y, pivot_z

disc = zcyl(140, 20, table_z).cut(box(-3, -80, 19, 3, 40, table_z + 1))       # blade slot
arm = box(30, 120, 20, 120, 270, table_z).fuse(box(14, 270, 20, 136, pivot_y + 30, table_z))
for x0, x1 in ((14, 28), (122, 136)):                                          # pivot cheeks
    cheek = box(x0, pivot_y - 20, table_z, x1, pivot_y + 20, pivot_z).fuse(xcyl(20, x0, x1, pivot_y, pivot_z))
    arm = arm.fuse(cheek.cut(xcyl(8.05, x0 - 1, x1 + 1, pivot_y, pivot_z)))
pointer = box(-5, -135, table_z, 5, -125, table_z + 2).fuse(box(-1.5, -166, table_z + 0.3, 1.5, -125, table_z + 1.3))
turntable = Component("turntable", name="Mitre turntable")
turntable.add("turntable", disc.fuse(arm).fuse(pointer).clean(), name="Turntable")
turntable.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
