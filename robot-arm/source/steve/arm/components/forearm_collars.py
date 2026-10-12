from steve import Component
from params import elbow_z, fa_y, fore_len
from shapes import ring, fuse

forearm_collars = Component("forearm_collars", name="Forearm collars")
collars = fuse(ring(44, 40, (90, fa_y, elbow_z), "X", 12), ring(44, 40, (fore_len - 90, fa_y, elbow_z), "X", 12))
forearm_collars.add("accent", collars, name="Blue collars")

forearm_collars.material("aluminum-6061-t6", finish="anodized", color="#2f6fd6")
