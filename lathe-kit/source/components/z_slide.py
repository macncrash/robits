"""Z slide (branch "milling"): rides the column dovetail (brass gib on the +Y side, M6 lock lever) and carries
the actuator: its pedestal bolts to the front face with the same 4 x M8 that held it to the headstock plate, so
moving the motor from lathe to mill is four screws. The Z ball nut sits in the block that reaches back into
the column's channel, flange on top.
"""
from steve import Component
from lathe_shapes import box, zcyl, xcyl
import cadquery as cq
from lathe_params import mill_spindle_y, mill_head_z

yc, hz = mill_spindle_y, mill_head_z
slide = box(95.1, yc - 60, 55, 127, yc + 60, 170)
groove = cq.Workplane("XY", origin=(0, 0, 54)).polyline(
    [(94.9, yc - 28.1), (105.1, yc - 35.15), (105.1, yc + 38.15), (94.9, yc + 31.1)]).close().extrude(117).val()
slide = slide.cut(groove)                            # dovetail + 0.1, +3 on +Y for the gib
for z in (hz + 15, hz - 59):                         # pedestal's 4 x M8, tapped 16 deep
    for dy in (-52, 52):
        slide = slide.cut(xcyl(3.4, 111, 127, yc + dy, z))
block = box(59, yc - 21, 140, 105.2, yc + 21, 170).cut(zcyl(12.05, 139.5, 170.5, 79, yc))
slide = slide.fuse(block)
slide = slide.cut(zcyl(3, 55, 75, 120, yc + 50))     # M6 lock lever onto the gib
z_slide = Component("z_slide", name="Z slide")
z_slide.add("slide", slide.clean(), name="Z slide")
z_slide.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
