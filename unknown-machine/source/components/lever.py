"""Quick-release cam lever: pivot pin through the band lug, two cam cheeks, arm lying back over the can."""
from steve import Component
from shapes import box, xcyl

lever = Component("lever", name="Clamp lever")
body = xcyl(2.5, -13, 13, 68, 26)
body = body.fuse(xcyl(6, 8.5, 12.5, 68, 26)).fuse(xcyl(6, -12.5, -8.5, 68, 26))
body = body.fuse(box(8.5, 63, 14, 12.5, 73, 26)).fuse(box(-12.5, 63, 14, -8.5, 73, 26))   # side bars past the lug, 4 x 10 deep
body = body.fuse(box(-12.5, 63, -38, 12.5, 73, 14)).fuse(xcyl(4, -14, 14, 70, -38))     # arm 10 deep, flush with the bars
lever.add("lever", body.clean(), name="Lever")
lever.material("aluminum-6061-t6", finish="anodized", color="#22283a")
