"""Cross-slide: rides the carriage's dovetail toward and away from the work (Y). Its SFU1204 ball screw runs in
a channel under the slide and down the carriage dovetail to the ball nut behind; the screw bracket and handwheel
are on the front end, so they move with the slide. A zero mark on the top faces the compound's degree scale.
"""
from steve import Component
from lathe_shapes import box, prism_xz, ycyl
from lathe_params import carriage_x, tool_y

xc = carriage_x + 35
body = box(xc - 30, -95, -77.9, xc + 30, -15, -56)
groove = [(xc - 20.1, -70), (xc + 23.1, -70), (xc + 19.05, -78.1), (xc - 16.05, -78.1)]   # +3 on +X for a gib
body = body.cut(prism_xz(groove, -96, -14))
body = body.cut(ycyl(6.5, -95, -14, xc, -75.2))      # channel for the ball screw
body = body.cut(box(xc - 0.2, tool_y - 31.5, -56.4, xc + 0.2, tool_y - 30.5, -56))       # zero mark for the compound
bracket = box(xc - 12, -101, -98, xc + 12, -95, -53)  # screw bearing bracket; zero line engraved by the dial's rim
bracket = bracket.cut(ycyl(5.05, -102, -94, xc, -75.2))
bracket = bracket.cut(box(xc - 0.2, -101, -57, xc + 0.2, -100.6, -53))
body = body.fuse(bracket)
cross_slide = Component("cross_slide", name="Cross-slide")
cross_slide.add("cross_slide", body.clean(), name="Cross-slide")
cross_slide.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
