"""Milling column (branch "milling"): 6061 column on a base plate that bolts to the bed where the headstock
plate was (the same 4 x M6). A 55-degree male dovetail up the front carries the Z slide; the SFU1204 Z screw
runs in a channel down the middle of the dovetail and turns in the cap at the top (Ø10 journal, two AXK1024
thrust washers), with the 200-line handwheel on top. Column 80 x 90 x 318 above the plate.
"""
from steve import Component
from lathe_shapes import box, zcyl
import cadquery as cq
from lathe_params import mill_spindle_y

yc = mill_spindle_y
plate = box(-40, -105, -98, 105, 70, -88)
for x in (-20, 70):                                  # M6 counterbored into the bed ways (the headstock plate's holes)
    for y in (-25, 25):
        plate = plate.cut(zcyl(3.3, -98, -88, x, y)).cut(zcyl(5.5, -94, -88, x, y))
column = box(15, yc - 45, -88, 95, yc + 45, 230)
dovetail = cq.Workplane("XY", origin=(0, 0, -88)).polyline(
    [(95, yc - 28), (105, yc - 35), (105, yc + 35), (95, yc + 28)]).close().extrude(318).val()
column = column.fuse(dovetail)
column = column.cut(box(57, yc - 22, -88, 106, yc + 22, 230))   # Z screw and nut channel
cap = box(15, yc - 45, 230, 95, yc + 45, 245).cut(zcyl(5.05, 229, 246, 79, yc))
cap = cap.cut(box(79 - 0.2, yc + 29.6, 241, 79 + 0.2, yc + 30, 245))   # zero line by the dial's rim
body = plate.fuse(column).fuse(cap)
for z in (-60, 0, 60, 120, 180):                     # lightening pockets in the back
    body = body.cut(box(14, yc - 30, z, 30, yc + 30, z + 40))
mill_column = Component("mill_column", name="Milling column")
mill_column.add("column", body.clean(), name="Column")
mill_column.material("aluminum-6061-t6", finish="anodized", color="#15171c")
