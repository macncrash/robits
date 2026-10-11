import cadquery as cq
from steve import Component
from params import elbow_z, fore_len, w_y
from shapes import cyl, fuse, V

wrist1 = Component("wrist1", name="Wrist 1 (J4 output, J5 mount)")
hub = cyl(50, (fore_len, w_y, elbow_z), "Y", 80).cut(cyl(44, (fore_len, w_y, elbow_z), "Y", 68))
boss = cyl(36, (fore_len + 39, w_y, elbow_z), "X", 22)
wrist1.add("body", fuse(hub, boss), name="Knuckle")

# Service cable loop from the knuckle to the J5 actuator, as in the tee art.
pts = [V(fore_len - 10, w_y + 30, elbow_z - 25), V(fore_len + 5, w_y + 52, elbow_z - 70),
       V(fore_len + 40, w_y + 55, elbow_z - 100), V(fore_len + 75, w_y + 40, elbow_z - 70),
       V(fore_len + 82, w_y + 20, elbow_z - 32)]
path = cq.Wire.assembleEdges([cq.Edge.makeSpline(pts)])
section = cq.Wire.makeCircle(6, pts[0], path.tangentAt(0))
cable = cq.Solid.sweep(section, [], path, True, True)
wrist1.add("cable", cable, op="new", name="Cable loop")

wrist1.material("aluminum-6061-t6", finish="anodized", color="#2a2e35")
wrist1.material("tpu-98a", bodies=["cable"], color="#111318")
