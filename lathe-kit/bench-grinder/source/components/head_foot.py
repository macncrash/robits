"""Head foot (cast iron, or a 6061 weldment): a saddle the barrel sits in (2 x M6 from below into the barrel)
on a 200 x 150 flange bolted to the stand's top plate with 4 x M8. A Ø16 hole lets the motor cable down into
the column."""
from steve import Component
from grinder_shapes import box, xcyl, zcyl
from grinder_params import spindle_z

z0 = spindle_z - 100                           # stand top plate
body = box(-100, -75, z0, 100, 75, z0 + 12).fuse(box(-38, -42, z0 + 12, 38, 42, spindle_z - 20))
body = body.cut(xcyl(54, -39, 39))
for x in (-80, 80):
    for y in (-55, 55):
        body = body.cut(zcyl(4.5, z0 - 1, z0 + 13, x, y))
for x in (-20, 20):
    body = body.cut(zcyl(3.3, z0 - 1, spindle_z - 40, x, 0)).cut(zcyl(5.5, z0 - 1, z0 + 7, x, 0))
body = body.cut(zcyl(8, z0 - 1, spindle_z - 40, 0, 0))
head_foot = Component("head_foot", name="Head foot")
head_foot.add("foot", body.clean(), name="Head foot")
head_foot.material("steel-s235jr", color="#2a2f3a")
