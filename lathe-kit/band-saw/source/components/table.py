"""Work table, 300 x 300 x 16, cast iron (a steel stand-in here), top ground: a Ø40 throat (for a phenolic insert),
a 2.5 mm blade-change slot to the front edge, and a 3/4 x 3/8 in miter slot 90 mm left of the blade. Tilts
0-45 degrees (left side down) on the trunnions: a cheek under the front and back edges carries an M8 stud through
each trunnion's arc slot, a five-lobe lock knob with a pointer onto the scale in front, a flanged nut behind."""
import cadquery as cq
from steve import Component
from bandsaw_shapes import box, ycyl, zcyl, prism_xz, tilt_point

top = box(-150, -150, -16, 150, 150, 0)
top = top.cut(zcyl(20, -17, 1)).cut(box(-1.5, -151, -17, 1.0, 0, 1))     # throat and blade slot
top = top.cut(box(-99.5, -151, -9.5, -80.5, 151, 1))                     # miter slot
cheek_pts = [(-20, -16), (50, -16), (50, -35), (30, -66), (5, -68), (-20, -40)]
body = top
sx, sz = tilt_point(60, 15)
for y0, y1, stud0, stud1 in ((-119, -111, -128, -119), (103, 111, 111, 120)):
    body = body.fuse(prism_xz(cheek_pts, y0, y1))
    body = body.fuse(ycyl(4, stud0, stud1, sx, sz))
knob = ycyl(18, -142, -128, sx, sz)
for k in range(5):
    lobe = cq.Solid.makeCylinder(5, 14, cq.Vector(sx, -142, sz + 18), cq.Vector(0, 1, 0))
    knob = knob.cut(lobe.rotate(cq.Vector(sx, 0, sz), cq.Vector(sx, 1, sz), 72 * k))
p0, p1 = tilt_point(58, 13), tilt_point(58, 17)
q0, q1 = tilt_point(82, 14.85), tilt_point(82, 15.15)
pointer = prism_xz([p0, q0, q1, p1], -129.5, -128)
nut = ycyl(9, 120, 123, sx, sz).fuse(ycyl(7.5, 123, 129, sx, sz))
body = body.fuse(knob).fuse(pointer).fuse(nut)
table = Component("table", name="Tilting work table")
table.add("table", body.clean(), name="Table")
table.material("steel-s235jr", color="#3a3d42")          # specified cast iron, ground top
