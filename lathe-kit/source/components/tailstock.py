"""Tailstock: base on the bed dovetail (brass gib, M8 lock bolt from the top), body with a 20 mm quill bore on
centre, quill lock (M6 lever) and the quill screw's end bearing. Slides along the bed by hand.
"""
from steve import Component
from lathe_shapes import box, prism_yz, xcyl, zcyl
from lathe_params import tailstock_x

x0, x1 = tailstock_x, tailstock_x + 70
base = box(x0, -62, -107.9, x1, 62, -80)
base = base.cut(prism_yz([(-40.1, -98), (43.1, -98), (35.96, -108.2), (-32.96, -108.2)], x0 - 1, x1 + 1))
base = base.cut(zcyl(4.25, -98, -80, x0 + 10, 45))                      # M8 lock bolt
body = box(x0 + 5, -28, -80, x1 - 5, 28, 0).fuse(xcyl(28, x0 + 5, x1 - 5))
body = body.cut(xcyl(10.05, x0, x1, 0, 0))                              # quill bore
body = body.cut(zcyl(3, 0, 29, x0 + 15, 0))                             # quill lock (M6), slit in the bore
end = xcyl(14, x1 - 5, x1 + 10).cut(xcyl(5.05, x1 - 6, x1 + 11))        # quill-screw bearing
end = end.cut(box(x1 + 9.6, -0.2, 10, x1 + 10, 0.2, 14))                # zero line by the dial's rim
tail = base.fuse(body).fuse(end)
tailstock = Component("tailstock", name="Tailstock")
tailstock.add("tailstock", tail.clean(), name="Tailstock")
tailstock.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
