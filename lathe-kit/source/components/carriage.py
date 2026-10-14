"""Carriage (saddle): rides the bed dovetail on a brass gib, carries the cross-slide dovetail on top and the
leadscrew nut in the apron at the front. Moved by hand with the leadscrew handwheel at the right end of the bed.
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
body = body.cut(ycyl(5.5, -63, 63, xc, -75.2))       # slot for the cross-feed screw
apron = box(xc - 20, -75, -130, xc + 20, -62, -100)   # leadscrew nut (Tr10 x 2, bronze insert)
apron = apron.cut(xcyl(5.25, xc - 21, xc + 21, -67.5, -120))
body = body.fuse(apron)
carriage = Component("carriage", name="Carriage (saddle)")
carriage.add("carriage", body.clean(), name="Carriage")
carriage.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
