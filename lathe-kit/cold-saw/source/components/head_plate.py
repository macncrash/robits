"""Head plate, 6061: carries the actuator on its pedestal (its 4 x M8), the worm gearbox on the bracket at the front
(bolted to the gearbox's back face), and the pivot knuckle at the back. Pivots down to cut."""
from steve import Component
from coldsaw_shapes import box, xcyl, zcyl
from coldsaw_params import gear_x, act_y, pivot_y, pivot_z

plate = box(gear_x - 70, 52, 113, gear_x + 70, 255, 125).fuse(box(30, 255, 113, 120, pivot_y, 125))
plate = plate.fuse(box(24, 52, 78, 124, 64, 125))                              # gearbox bracket
plate = plate.fuse(xcyl(20, 30, 120, pivot_y, pivot_z)).cut(xcyl(8.05, 29, 121, pivot_y, pivot_z))
for dx in (-52, 52):                                                           # pedestal's 4 x M8, tapped
    for dy in (15, -59):
        plate = plate.cut(zcyl(3.4, 109, 125, gear_x + dx, act_y + dy))
head_plate = Component("head_plate", name="Head plate")
head_plate.add("plate", plate.clean(), name="Head plate")
head_plate.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
