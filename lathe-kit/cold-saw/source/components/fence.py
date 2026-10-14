"""Fence (the vise's fixed jaw), 6061 with hardened steel faces: two halves either side of the blade, bolted to
the base's side pads, clear of the turntable underneath. A mm rule is engraved along the top of the right half
(a line every 5 mm, long every 10, from the blade)."""
from steve import Component
from coldsaw_shapes import box, zcyl
from coldsaw_params import table_z

f = box(-260, 0, table_z, -35, 20, 75).fuse(box(35, 0, table_z, 260, 20, 75))
f = f.cut(zcyl(210, table_z - 1, table_z + 0.5))                            # clear of the turntable and its arm
for k in range(1, 45):
    x = 35 + 5 * k
    length = 8 if k % 2 == 0 else 4
    f = f.cut(box(x - 0.2, 20 - length, 74.6, x + 0.2, 20.5, 76))
fence = Component("fence", name="Fence (fixed jaw)")
fence.add("fence", f.clean(), name="Fence")
fence.material("aluminum-6061-t6", finish="anodized", color="#2a3140")
