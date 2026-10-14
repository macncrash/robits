"""Table trunnions (6061, black), one in front of the table's cheeks and one behind, bolted to the frame's
shelf: sector plates about the table's tilt axis (along Y through the blade line on the table top), so the table
tilts on a virtual pivot and the blade stays in its slot. Each has an arc slot for its lock stud. The front one
is engraved 0-45 degrees (a line every degree, long every 5, longer every 15), read by the pointer on the lock
knob."""
from steve import Component
from bandsaw_shapes import box, tilt_sector, tilt_point, prism_xz, one
import cadquery as cq


def slot(y0, y1):
    s = tilt_sector(55.8, 64.2, 15, 60, y0, y1)
    for a in (15, 60):
        x, z = tilt_point(60, a)
        s = s.fuse(cq.Solid.makeCylinder(4.2, y1 - y0, cq.Vector(x, y0, z), cq.Vector(0, 1, 0)))
    return s


def side(y0, y1, scale_face=None):
    plate = tilt_sector(40, 80, -10, 75, y0, y1).fuse(box(-14, y0, -85, 40, y1, -78))
    plate = plate.cut(box(-100, y0 - 1, -19, 100, y1 + 1, 1))               # 3 mm under the table
    plate = plate.cut(slot(y0 - 1, y1 + 1))
    if scale_face is not None:
        for k in range(46):
            length = 8 if k % 15 == 0 else (6 if k % 5 == 0 else 4)
            a = 15 + k
            pts = [tilt_point(80 - length, a), tilt_point(80.5, a), tilt_point(80.5, a + 0.3),
                   tilt_point(80 - length, a + 0.3)]
            plate = plate.cut(prism_xz(pts, scale_face, scale_face + 0.4))
    return plate.clean()


trunnions = Component("trunnions", name="Table trunnions with 0-45 degree scale")
trunnions.add("trunnions", one(side(-128, -120, scale_face=-128), side(112, 120)), name="Front and back trunnions")
trunnions.material("aluminum-6061-t6", finish="anodized", color="#15171c")
