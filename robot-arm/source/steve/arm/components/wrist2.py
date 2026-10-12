from steve import Component
from params import elbow_z, w2_x, w_y, a6_z
from shapes import cyl, box, fuse

wrist2 = Component("wrist2", name="Wrist 2 (J5 output, J6 mount)")
hub = cyl(45, (w2_x, w_y, elbow_z), "X", 30).cut(cyl(39, (w2_x, w_y, elbow_z), "X", 18))
# Neck kept within the hub's 30 mm length so it clears the J5 output face; it reaches down to the J6 top.
neck_top, neck_bottom = elbow_z - 23, a6_z + 42.5
neck = box(30, 60, neck_top - neck_bottom, (w2_x, w_y, (neck_top + neck_bottom) / 2), fillet_z=0)
wrist2.add("body", fuse(hub, neck), name="Knuckle")

wrist2.material("aluminum-6061-t6", finish="anodized", color="#2a2e35")
