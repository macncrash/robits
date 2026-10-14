"""4-way tool post (34CrNiMo6 / AISI 4340 QT; 4140 if that is what the shop has): four 10 mm pockets for 8 mm square HSS bits on a 1 mm shim, so the
cutting edge sits on centre height; 2 x M6 clamp screws per side; turns on a centre M8 stud with a lever nut.
"""
from steve import Component
from lathe_shapes import box, zcyl
from lathe_params import carriage_x, tool_y

xc, yc = carriage_x + 35, tool_y
post = box(xc - 18, yc - 18, -24, xc + 18, yc + 18, -9)              # base
post = post.fuse(box(xc - 8, yc - 8, -9, xc + 8, yc + 8, 1))           # centre column between the pockets
post = post.fuse(box(xc - 18, yc - 18, 1, xc + 18, yc + 18, 12))       # cap carrying the clamp screws
post = post.cut(zcyl(4.25, -24, 12, xc, yc))                           # M8 stud
for dx, dy in ((-9, 13), (9, 13), (-9, -13), (9, -13), (13, -9), (13, 9), (-13, -9), (-13, 9)):
    post = post.cut(zcyl(2.5, 1, 12, xc + dx, yc + dy))                # M6 tapped clamp screws
tool_post = Component("tool_post", name="4-way tool post")
tool_post.add("post", post.clean(), name="Tool post")
tool_post.material("steel-34crnimo6", finish="machined", color="#3a3d42")
