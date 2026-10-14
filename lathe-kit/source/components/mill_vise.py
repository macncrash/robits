"""Machine vise for the milling attachment (branch "milling"): 60 wide jaws, opens to 45, on the cross-slide in
place of the compound (it goes on the compound's M8 pivot stud, so it swivels; square it with the zero mark).
Body, fixed jaw (rear) and the screw block (front) are one 6061 piece; hardened steel jaw plates."""
from steve import Component
from lathe_shapes import box, zcyl, ycyl
from lathe_params import carriage_x, tool_y

xc = carriage_x + 35
body = box(xc - 30, -94, -56, xc + 30, -17, -44)                    # base on the cross-slide top
body = body.cut(zcyl(4.25, -56, -44, xc, tool_y)).cut(zcyl(7.5, -50, -44, xc, tool_y))   # M8 stud, nut counterbore
body = body.fuse(box(xc - 30, -30, -44, xc + 30, -17, -16))         # fixed jaw
body = body.fuse(box(xc - 30, -94, -44, xc + 30, -86, -20))         # screw block
body = body.cut(ycyl(5.1, -95, -85, xc, -30))                       # M10 vise screw
body = body.cut(box(xc - 4, -84, -46, xc + 4, -30, -44))            # slot for the moving jaw's nut
mill_vise = Component("mill_vise", name="Milling vise 60 mm")
mill_vise.add("body", body.clean(), name="Vise body")
mill_vise.material("aluminum-6061-t6", finish="anodized", color="#2a3140")
