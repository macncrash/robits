import math
from steve import Component
from params import base_h
from shapes import cyl, ring, fuse

base = Component("base", name="Pedestal base")

foot = cyl(115, (0, 0, 8), "Z", 16)
heads = []
for k in range(4):
    a = math.radians(45 + 90 * k)
    x, y = 100 * math.cos(a), 100 * math.sin(a)
    foot = foot.cut(cyl(6, (x, y, 8), "Z", 20))
    heads.append(cyl(9, (x, y, 19), "Z", 6))
step = cyl(95, (0, 0, 25), "Z", 18)
column = cyl(80, (0, 0, 65), "Z", 62)
for z in (48, 60, 72):
    column = column.cut(ring(81, 78, (0, 0, z), "Z", 3))
top = cyl(75, (0, 0, base_h - 3), "Z", 6)
connector = cyl(13, (-88, 0, 62), "X", 20)
body = fuse(foot, step, column, top, connector).cut(cyl(70, (0, 0, 60), "Z", 88))  # cast shell, 8-10 mm walls
base.add("body", body, name="Pedestal")
base.add("accent", ring(84, 74, (0, 0, base_h - 10), "Z", 8), op="new", name="Blue ring")
base.add("bolts", fuse(*heads), op="new", name="Anchor bolts")

base.material("aluminum-6061-t6", finish="powder-coated", color="#23272e")
base.material("aluminum-6061-t6", bodies=["accent"], finish="anodized", color="#2f6fd6")
base.material("stainless-304", bodies=["bolts"], finish="brushed")
