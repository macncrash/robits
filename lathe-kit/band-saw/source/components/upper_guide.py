"""Upper blade guide on its sliding post: a 20 x 20 ground steel post in the frame's bushing (lock knob on the
right), carrying a head that straddles the blade with two bronze side blocks set 0.1 mm off it and a hardened
thrust face 0.5 mm behind its back. Set the head just above the work. The post's left face is engraved every
5 mm (long every 10, 0 to 100): read against the bushing's bottom edge, it is the height under the guide. Modelled
40 mm above the table (guide_z 60 less the 20 mm head)."""
from steve import Component
from bandsaw_shapes import box, one
from bandsaw_params import guide_z

h = guide_z
post = box(-10, 45, h, 10, 65, h + 300)
for v in range(0, 101, 5):                      # mark for v mm under the guide sits at the bushing edge (z 250)
    z = 250 + (h - v)
    length = 10 if v % 10 == 0 else 5
    post = post.cut(box(-10, 45, z - 0.3, -9.6, 45 + length, z + 0.3))
arm = box(-10, 7, h, 10, 65, h + 30)
blocks = box(-16, -8, h + 2, -0.75, 8, h + 28).fuse(box(0.1, -8, h + 2, 16, 8, h + 28))
upper_guide = Component("upper_guide", name="Upper blade guide and post")
upper_guide.add("guide", one(post.fuse(arm).clean(), blocks.clean()), name="Guide post, head and bronze side blocks")
upper_guide.material("steel-1c60", finish="polished")
