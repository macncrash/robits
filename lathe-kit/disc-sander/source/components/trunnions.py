"""Table trunnions, one each side of the table (6061, black): fixed sector plates on posts bolted to the stand top.
Each has two arc slots about the table's tilt axis (the table's near edge, x along the abrasive face at y -100,
z -20), so the table swings on a virtual pivot and its edge stays 3.5 mm from the disc at every angle. A 0-45
degree scale (1 degree lines, long every 5, longer every 15) is engraved on the outer face, read by the pointer
on the table's lock knob.
"""
import cadquery as cq
from steve import Component
from sander_shapes import box, sector_yz, prism_yz, trunnion_point
from sander_params import table_y, table_z, base_z, riser_h

top = base_z - riser_h
py, pz = table_y, table_z


def slot(r, a0, a1, x0, x1):
    """Arc slot for an M8 stud (8.4 wide) with round ends."""
    s = sector_yz(r - 4.2, r + 4.2, a0, a1, py, pz, x0, x1)
    for a in (a0, a1):
        y, z = trunnion_point(r, a, py, pz)
        s = s.fuse(cq.Solid.makeCylinder(4.2, x1 - x0, cq.Vector(x0, y, z), cq.Vector(1, 0, 0)))
    return s


def side(x0, x1, outer):
    plate = sector_yz(36, 84, 15, 85, py, pz, x0, x1)
    plate = plate.fuse(box(x0, -140, top, x1, -104, -80))                 # post
    fx = (x1, x1 + 26) if outer > x0 else (x0 - 26, x0)
    plate = plate.fuse(box(min(fx[0], x0), -150, top, max(fx[1], x1), -100, top + 6))   # foot
    plate = plate.cut(slot(50, 30, 75, x0 - 1, x1 + 1)).cut(slot(64, 20, 65, x0 - 1, x1 + 1))
    for k in range(46):                                                   # scale: line k at 30 + k degrees
        length = 8 if k % 15 == 0 else (6 if k % 5 == 0 else 4)
        a = 30 + k
        p0, p1 = trunnion_point(84 - length, a, py, pz), trunnion_point(84.5, a, py, pz)
        q0, q1 = trunnion_point(84 - length, a + 0.25, py, pz), trunnion_point(84.5, a + 0.25, py, pz)
        line = prism_yz([p0, p1, q1, q0], outer - 0.4 if outer > x0 else outer, outer if outer > x0 else outer + 0.4)
        plate = plate.cut(line)
    return plate.clean()


trunnions = Component("trunnions", name="Table trunnions with 0-45 degree scale")
trunnions.add("right", side(126, 134, 134), name="Right trunnion")
trunnions.add("left", side(-134, -126, -134), name="Left trunnion")
trunnions.material("aluminum-6061-t6", finish="anodized", color="#15171c")
