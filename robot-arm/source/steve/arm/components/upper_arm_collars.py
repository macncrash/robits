from steve import Component
from params import shoulder_z, elbow_z, ua_y
from shapes import ring, fuse

upper_arm_collars = Component("upper_arm_collars", name="Upper arm collars")
collars = fuse(ring(52, 47.5, (0, ua_y, shoulder_z + 80), "Z", 12), ring(52, 47.5, (0, ua_y, elbow_z - 80), "Z", 12))
upper_arm_collars.add("accent", collars, name="Blue collars")

upper_arm_collars.material("aluminum-6061-t6", finish="anodized", color="#2f6fd6")
