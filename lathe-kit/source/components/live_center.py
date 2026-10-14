"""MT1 live centre (bought): 60-degree point on bearings; envelope at catalogue size."""
import cadquery as cq
from steve import Component
from lathe_shapes import xcyl
from lathe_params import tailstock_x

x_nose = tailstock_x - 30
shank = cq.Solid.makeCone(6.03, 4.7, 53, cq.Vector(x_nose, 0, 0), cq.Vector(1, 0, 0))
body = xcyl(12.5, x_nose - 20, x_nose).fuse(xcyl(8, x_nose - 28, x_nose - 20))
point = cq.Solid.makeCone(0.01, 8, 13.86, cq.Vector(x_nose - 41.86, 0, 0), cq.Vector(1, 0, 0))
live_center = Component("live_center", name="Live centre MT1 (bought)")
live_center.add("centre", shank.fuse(body).fuse(point).clean(), name="Live centre")
live_center.material("steel-1c60", finish="polished")
