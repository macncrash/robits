"""Welded stand, S235: 50 x 50 x 3 box-section legs and rails, 10 mm top plate (800 x 640), 6 mm shelf for the
coolant tank, M12 levelling feet. The chip tray sits on the top plate."""
from steve import Component
from coldsaw_shapes import box, zcyl
from coldsaw_params import floor_z

s = box(-400, -260, -10, 400, 380, 0)
for x0 in (-380, 330):
    for y0 in (-240, 310):
        s = s.fuse(box(x0, y0, floor_z + 20, x0 + 50, y0 + 50, -10))
        s = s.fuse(zcyl(25, floor_z, floor_z + 20, x0 + 25, y0 + 25))   # levelling foot
for z0 in (-60, -700):                                                  # top rails and shelf rails
    s = s.fuse(box(-330, -240, z0, 330, -190, z0 + 50)).fuse(box(-330, 310, z0, 330, 360, z0 + 50))
    s = s.fuse(box(-380, -190, z0, -330, 310, z0 + 50)).fuse(box(330, -190, z0, 380, 310, z0 + 50))
s = s.fuse(box(-330, -190, -656, 330, 310, -650))                     # shelf
s = s.cut(zcyl(10.5, -11, 1, -300, 280))                               # tray drain
stand = Component("stand", name="Stand")
stand.add("stand", s.clean(), name="Stand")
stand.material("steel-s235jr", color="#1f2227")
