from steve import Component
from params import elbow_z, fa_y, fore_len
from shapes import cyl, ring, fuse

# The blue collars are their own component (forearm_collars) so the tube is one solid for stress studies.

forearm = Component("forearm", name="Forearm")
hub = cyl(58, (0, fa_y, elbow_z), "Y", 70).cut(cyl(52, (0, fa_y, elbow_z), "Y", 58))
tube = ring(40, 36, (fore_len / 2, fa_y, elbow_z), "X", fore_len)  # 4 mm wall
tube = tube.cut(cyl(52, (fore_len, fa_y, elbow_z), "Y", 120))
# Trim the tube flush with the hub faces so it clears the J3 actuator (fit check: 2157 mm3 overlap).
for y_side in (fa_y + 35 + 15, fa_y - 35 - 15):
    tube = tube.cut(cyl(66, (0, y_side, elbow_z), "Y", 30))
forearm.add("body", fuse(hub, tube), name="Hub and tube")

forearm.material("aluminum-6061-t6", finish="anodized", color="#2a2e35")
