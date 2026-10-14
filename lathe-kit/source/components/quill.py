"""Tailstock quill: 20 mm, MT1 taper in the nose, Tr10 x 2 nut at the back; engraved 0-35 mm along the top
(a line every mm, a long one every 5) so the drilling depth reads straight off the quill."""
from steve import Component
from lathe_shapes import xcyl, box
from lathe_params import tailstock_x
import cadquery as cq

x_nose = tailstock_x - 30                                                # extends 35 mm from the body face
quill = xcyl(10, x_nose, tailstock_x + 65)
taper = cq.Solid.makeCone(6.03, 4.7, 53, cq.Vector(x_nose, 0, 0), cq.Vector(1, 0, 0))   # MT1 (1:20)
quill = quill.cut(taper).cut(xcyl(5.2, x_nose + 53, tailstock_x + 66))
for k in range(36):                                                      # depth scale, 0 at the body face
    x = tailstock_x + 5 - k
    length = 4 if k % 5 == 0 else 2
    quill = quill.cut(box(x - 0.15, -length / 2, 9.7, x + 0.15, length / 2, 10.5))
quill_c = Component("quill", name="Tailstock quill")
quill_c.add("quill", quill.clean(), name="Quill")
quill_c.material("steel-1c60", finish="polished")
