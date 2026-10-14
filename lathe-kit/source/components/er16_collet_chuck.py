"""Tailstock collet chuck (bought): MT1 shank, ER16 nut (Ø32), takes standard ER16 collets for 1-10 mm drills and
reamers; envelope at catalogue size, in the quill in place of the live centre."""
import cadquery as cq
from steve import Component
from lathe_shapes import xcyl
from lathe_params import tailstock_x

x_nose = tailstock_x - 30
shank = cq.Solid.makeCone(6.03, 4.7, 53, cq.Vector(x_nose, 0, 0), cq.Vector(1, 0, 0))   # MT1
body = xcyl(12.5, x_nose - 12, x_nose).fuse(xcyl(16, x_nose - 30, x_nose - 12)).fuse(xcyl(9, x_nose - 34, x_nose - 30))
chuck = shank.fuse(body).cut(xcyl(3.05, x_nose - 35, x_nose - 8))      # collet bore with a 6 mm drill in it
er16_collet_chuck = Component("er16_collet_chuck", name="ER16 collet chuck, MT1 shank (bought)")
er16_collet_chuck.add("chuck", chuck.clean(), name="Collet chuck")
er16_collet_chuck.material("steel-1c45", finish="polished")
