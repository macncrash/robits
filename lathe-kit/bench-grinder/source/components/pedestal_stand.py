"""Pedestal stand (S235 weldment): 420 x 420 x 12 base plate with 4 x Ø14 holes to bolt it to the floor, a
Ø101.6 x 3.6 tube column, a 260 x 200 x 15 top plate (4 x Ø9 for the head foot, access holes for its barrel
screws, a Ø24 cable hole into the column) and six gussets. Spindle at 1020 mm from the floor."""
from steve import Component
from grinder_shapes import box, zcyl, prism_xz, prism_yz
from grinder_params import spindle_z

top = spindle_z - 100
base = box(-210, -210, 0, 210, 210, 12)
for x in (-170, 170):
    for y in (-170, 170):
        base = base.cut(zcyl(7, -1, 13, x, y))
column = zcyl(50.8, 12, top - 15).cut(zcyl(47.2, 11, top - 14))
plate = box(-130, -100, top - 15, 130, 100, top)
for x in (-80, 80):
    for y in (-55, 55):
        plate = plate.cut(zcyl(4.5, top - 16, top + 1, x, y))
for x in (-20, 20):
    plate = plate.cut(zcyl(9, top - 16, top + 1, x, 0))
plate = plate.cut(zcyl(12, top - 16, top + 1, 0, 0))
body = base.fuse(column).fuse(plate)
for s in (1, -1):                              # base gussets along X and Y, top gussets along X
    body = body.fuse(prism_xz([(s * 49, 12), (s * 160, 12), (s * 49, 132)], -3, 3))
    body = body.fuse(prism_yz([(s * 49, 12), (s * 160, 12), (s * 49, 132)], -3, 3))
    body = body.fuse(prism_xz([(s * 49, top - 15), (s * 115, top - 15), (s * 49, top - 75)], -3, 3))
pedestal_stand = Component("pedestal_stand", name="Pedestal stand")
pedestal_stand.add("stand", body.clean(), name="Stand")
pedestal_stand.material("steel-s235jr", color="#20242c")
