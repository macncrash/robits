from steve import Component
from params import shoulder_z, elbow_z, ua_y, upper_len
from shapes import cyl, ring, fuse

# The blue collars are their own component (upper_arm_collars) so the tube is one solid for stress studies.

upper_arm = Component("upper_arm", name="Upper arm")
hub = cyl(65, (0, ua_y, shoulder_z), "Y", 122).cut(cyl(59, (0, ua_y, shoulder_z), "Y", 110))
tube = ring(47.5, 42.5, (0, ua_y, (shoulder_z + elbow_z) / 2), "Z", upper_len)  # 5 mm wall
tube = tube.cut(cyl(62, (0, ua_y, elbow_z), "Y", 130))
upper_arm.add("body", fuse(hub, tube), name="Hub and tube")

upper_arm.material("aluminum-6061-t6", finish="anodized", color="#2a2e35")
