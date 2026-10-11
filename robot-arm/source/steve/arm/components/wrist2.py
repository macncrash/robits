from steve import Component
from params import elbow_z, w2_x, w_y
from shapes import cyl, fuse

wrist2 = Component("wrist2", name="Wrist 2 (J5 output, J6 mount)")
hub = cyl(45, (w2_x, w_y, elbow_z), "X", 30).cut(cyl(39, (w2_x, w_y, elbow_z), "X", 18))
neck = cyl(30, (w2_x, w_y, elbow_z - 34), "Z", 22)
wrist2.add("body", fuse(hub, neck), name="Knuckle")

wrist2.material("aluminum-6061-t6", finish="anodized", color="#2a2e35")
