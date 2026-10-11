from steve import Component
from params import elbow_z, fa_y, fore_len
from shapes import cyl, ring, fuse

forearm = Component("forearm", name="Forearm")
hub = cyl(58, (0, fa_y, elbow_z), "Y", 70).cut(cyl(52, (0, fa_y, elbow_z), "Y", 58))
tube = ring(40, 36, (fore_len / 2, fa_y, elbow_z), "X", fore_len)  # 4 mm wall
tube = tube.cut(cyl(52, (fore_len, fa_y, elbow_z), "Y", 120))
forearm.add("body", fuse(hub, tube), name="Hub and tube")
collars = fuse(ring(44, 40, (90, fa_y, elbow_z), "X", 12), ring(44, 40, (fore_len - 90, fa_y, elbow_z), "X", 12))
forearm.add("accent", collars, op="new", name="Blue collars")

forearm.material("aluminum-6061-t6", finish="anodized", color="#2a2e35")
forearm.material("aluminum-6061-t6", bodies=["accent"], finish="anodized", color="#2f6fd6")
