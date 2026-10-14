"""Lower blade guide, under the table on the frame's shelf: the same side blocks and thrust face as the upper
guide, on a fixed post. Its top is 42 mm under the table so the table tilts to 45 degrees over it."""
from steve import Component
from bandsaw_shapes import box, one

post = box(-10, 20, -85, 10, 40, -42).fuse(box(-10, 7, -70, 10, 40, -42))
blocks = box(-16, -8, -68, -0.75, 8, -44).fuse(box(0.1, -8, -68, 16, 8, -44))
lower_guide = Component("lower_guide", name="Lower blade guide")
lower_guide.add("guide", one(post.clean(), blocks.clean()), name="Guide post, head and bronze side blocks")
lower_guide.material("steel-1c60", finish="machined")
