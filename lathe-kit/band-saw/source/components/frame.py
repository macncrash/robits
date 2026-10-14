"""Saw frame: a welded and machined steel C-frame (as a small cast-iron saw's casting would be). A column (spine)
on the right, x 280-330, stands on the stand top on a base flange and carries the upper and lower wheel plates
behind the wheels; the throat between the blade and the column is 280 mm. Between the plates, at table height,
the frame is open behind the blade. The lower plate carries the driven wheel's shaft in a bearing boss (two
6204-2RS); the upper plate has a vertical slot for the idler wheel's tension slider. On top of the lower
plate a shelf carries the table trunnions and the lower blade guide; a channel in front of the column guards
the blade's return run. Behind: the guide-post bushing with its lock knob, the tension-screw bracket, and a
blade-tension scale beside the slot (lines for 6, 10 and 13 mm blades and slack).
"""
from steve import Component
from bandsaw_shapes import box, xcyl, ycyl, zcyl
from bandsaw_params import lower_z, upper_z, stand_top

upper = box(-40, 30, 140, 330, 42, 455)
upper = upper.cut(box(114, 29, upper_z - 30, 136, 43, upper_z + 30))        # tension slot
for length, z in ((10, upper_z - 6), (6, upper_z - 2), (10, upper_z + 2), (6, upper_z + 6)):
    upper = upper.cut(box(140, 41.6, z - 0.3, 140 + length, 42, z + 0.3))   # tension scale on the back face
lower = box(-40, 30, -390, 330, 42, -100)
lower = lower.fuse(ycyl(30, 42, 52, 125, lower_z))                          # bearing boss
lower = lower.cut(ycyl(10.5, 29, 53, 125, lower_z))
spine = box(280, -50, stand_top + 10, 330, 42, 455)
flange = box(270, -80, stand_top, 345, 60, stand_top + 10)
shelf = box(-60, -135, -100, 280, 125, -85)
shelf = shelf.cut(box(-8, -14, -101, 8, 14, -84)).cut(box(242, -16, -101, 262, 16, -84))   # blade slots
channel = box(238, -22, -100, 280, 22, 140).cut(box(242, -16, -101, 262, 16, 141))         # return-run guard
bushing = box(-16, 42, 250, 16, 71, 300).cut(box(-10.1, 44.9, 249, 10.1, 65.1, 301))
lock = xcyl(4, 16, 30, 55, 275).fuse(xcyl(10, 30, 40, 55, 275))              # guide-post lock knob
bracket = box(105, 42, 440, 145, 75, 452).cut(zcyl(5.5, 439, 453, 125, 58))
body = upper.fuse(lower).fuse(spine).fuse(flange).fuse(shelf).fuse(channel).fuse(bushing).fuse(lock).fuse(bracket)
for x in (285, 335):                                                        # 4 x M10 into the stand top
    for y in (-70, 50):
        body = body.cut(zcyl(5.5, stand_top - 1, stand_top + 11, x, y))
frame = Component("frame", name="Saw frame (C-frame)")
frame.add("frame", body.clean(), name="C-frame")
frame.material("steel-s235jr", color="#2b2f36")
