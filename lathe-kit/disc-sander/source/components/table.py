"""Work table, 6061 (black, top faced): 250 x 160, 16 thick, a 3/4 x 3/8 in miter slot parallel to the disc, the
near edge 3.5 mm from the abrasive and bevelled underneath so it stays clear when tilted. Tilts 0-45 degrees down
on the two trunnions: a cheek plate under each side carries two M8 studs through the trunnion's arc slots; one
stud has a lock knob with a pointer onto the degree scale, the other a flanged lock nut.
"""
import cadquery as cq
from steve import Component
from sander_shapes import box, xcyl, prism_yz, trunnion_point
from sander_params import table_y, table_z

py, pz = table_y, table_z
t = 16
plate = prism_yz([(py, pz), (py - 160, pz), (py - 160, pz - t), (py - t, pz - t)], -125, 125)
slot_y = py - 60                                     # miter slot centre, 19.05 x 9.5
plate = plate.cut(box(-126, slot_y - 9.525, pz - 9.5, 126, slot_y + 9.525, pz + 1))

cheek_pts = [trunnion_point(24, 42, py, pz), trunnion_point(72, 42, py, pz), trunnion_point(72, 30, py, pz),
             trunnion_point(72, 15, py, pz), (trunnion_point(72, 15, py, pz)[0], pz - t + 0.01),
             (py - t - 8, pz - t + 0.01)]
body = plate
for x0, x1, out in ((117, 125, 1), (-125, -117, -1)):
    body = body.fuse(prism_yz(cheek_pts, x0, x1))
    face = x1 if out > 0 else x0                     # outer face of the cheek
    tr = face + out * 9                              # outer face of the trunnion plate (1 mm gap + 8)
    for r, a, knob in ((50, 30, True), (64, 20, False)):
        y, z = trunnion_point(r, a, py, pz)
        stud = xcyl(4, min(face, tr), max(face, tr), y, z)
        if knob:                                     # 5-lobe knob, Ø36, 14 long, and a pointer onto the scale
            head = xcyl(18, min(tr, tr + out * 14), max(tr, tr + out * 14), y, z)
            for k in range(5):
                lobe = cq.Solid.makeCylinder(5, 14, cq.Vector(min(tr, tr + out * 14), y, z + 18),
                                             cq.Vector(1, 0, 0))
                head = head.cut(lobe.rotate(cq.Vector(0, y, z), cq.Vector(1, 0, 0), 72 * k))
            q0, q1 = trunnion_point(r + 32, a - 0.3, py, pz), trunnion_point(r + 32, a + 0.3, py, pz)
            ptr = prism_yz([trunnion_point(r - 2, a - 2, py, pz), trunnion_point(r - 2, a + 2, py, pz), q1, q0],
                           min(tr, tr + out * 1.5), max(tr, tr + out * 1.5))
            head = head.fuse(ptr)
        else:                                        # flanged M8 nut with washer
            head = xcyl(9, min(tr, tr + out * 3), max(tr, tr + out * 3), y, z)
            head = head.fuse(xcyl(7.5, min(tr, tr + out * 9), max(tr, tr + out * 9), y, z))
        body = body.fuse(stud).fuse(head)
table = Component("table", name="Tilting work table with miter slot")
table.add("table", body.clean(), name="Table")
table.material("aluminum-6061-t6", finish="anodized", color="#15171c")
