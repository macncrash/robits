"""Carriage (saddle): rides the bed dovetail on a brass gib, carries the cross-slide dovetail on top and the
leadscrew's ball nut in the housing at the front. Moved by hand with the leadscrew handwheel at the right end of
the bed. The cross-slide's ball nut sits in the block behind the slide; the cross screw runs in a channel down the
middle of the dovetail. The printed way covers screw to the two ends (2 x M4 each).
"""
from steve import Component
from lathe_shapes import box, prism_yz, prism_xz, xcyl, ycyl, zcyl
from lathe_params import carriage_x

x0, x1 = carriage_x, carriage_x + 70
xc = (x0 + x1) / 2
body = box(x0, -62, -107.9, x1, 62, -78)
groove = [(-40.1, -98), (43.1, -98), (35.96, -108.2), (-32.96, -108.2)]   # bed dovetail + 0.1, +3 on +Y for the gib
body = body.cut(prism_yz(groove, x0 - 1, x1 + 1))
for x in (x0 + 12, xc, x1 - 12):                     # 3 x M4 gib adjusting screws from the back
    body = body.cut(ycyl(1.65, 30, 62, x, -103))
body = body.cut(zcyl(2.5, -98, -78, x1 - 8, -50))    # carriage lock screw (M5) down onto the ways
dovetail = [(xc - 16, -78), (xc + 16, -78), (xc + 20, -70), (xc - 20, -70)]   # cross-slide ways along Y
body = body.fuse(prism_xz(dovetail, -62, 62))
nut_block = box(xc - 22, -8, -80, xc + 22, 22, -58)  # cross-slide ball nut, flange on the back face
body = body.fuse(nut_block)
body = body.cut(ycyl(6.5, -63, 63, xc, -75.2))       # channel for the cross screw
body = body.cut(ycyl(12.05, -8.5, 22.5, xc, -75.2))   # nut bore
body = body.cut(box(xc - 21, 22, -86, xc + 21, 33, -54))   # recess for the nut flange (through the dovetail)
housing = box(xc - 20, -84, -137, xc + 20, -52, -100)   # leadscrew ball nut, flange on the right-hand face
housing = housing.cut(xcyl(12.05, xc - 10.5, xc + 21, -67.5, -120))
housing = housing.cut(xcyl(6.5, xc - 21, xc - 10, -67.5, -120))
body = body.fuse(housing)
body = body.cut(box(xc + 20, -88, -141, xc + 31, -57, -99))   # clear the leadscrew nut's flange
for x in (x0, x1):                                   # M4 tapped for the way covers
    for y in (-40, 40):
        body = body.cut(xcyl(1.65, x - 10 if x == x1 else x, x if x == x1 else x + 10, y, -86))
carriage = Component("carriage", name="Carriage (saddle)")
carriage.add("carriage", body.clean(), name="Carriage")
carriage.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
