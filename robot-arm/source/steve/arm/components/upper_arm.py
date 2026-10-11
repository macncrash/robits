from steve import Component
from params import shoulder_z, elbow_z, ua_y, upper_len
from shapes import cyl, ring, fuse

upper_arm = Component("upper_arm", name="Upper arm")
hub = cyl(65, (0, ua_y, shoulder_z), "Y", 122).cut(cyl(59, (0, ua_y, shoulder_z), "Y", 110))
tube = ring(47.5, 42.5, (0, ua_y, (shoulder_z + elbow_z) / 2), "Z", upper_len)  # 5 mm wall
tube = tube.cut(cyl(62, (0, ua_y, elbow_z), "Y", 130))
upper_arm.add("body", fuse(hub, tube), name="Hub and tube")
collars = fuse(ring(52, 47.5, (0, ua_y, shoulder_z + 80), "Z", 12), ring(52, 47.5, (0, ua_y, elbow_z - 80), "Z", 12))
upper_arm.add("accent", collars, op="new", name="Blue collars")

upper_arm.material("aluminum-6061-t6", finish="anodized", color="#2a2e35")
upper_arm.material("aluminum-6061-t6", bodies=["accent"], finish="anodized", color="#2f6fd6")
