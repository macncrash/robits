"""Motor plate (12 mm steel) under the actuator's pedestal: hinged along its back edge to the stand top, with a
jack screw at the front, so lowering the front tilts the actuator away from the lower wheel and tensions the
belt (an old-school motor platform). The pedestal's 4 x M8 are tapped into it."""
from steve import Component
from bandsaw_shapes import box, xcyl, zcyl, one
from bandsaw_params import stand_top, motor_y

top = stand_top + 12
plate = box(40, -110, stand_top, 210, 95, top)
for x in (125 - 52, 125 + 52):                       # pedestal holes (actuator z -15 and 59)
    for az in (-15, 59):
        plate = plate.cut(zcyl(3.4, stand_top - 1, top + 1, x, az + motor_y))
hinge = xcyl(7, 40, 210, 102, stand_top + 7)
jack = zcyl(5, stand_top, stand_top + 20, 125, -100).fuse(zcyl(12, stand_top + 20, stand_top + 28, 125, -100))
motor_plate = Component("motor_plate", name="Hinged motor plate")
motor_plate.add("plate", one(plate.fuse(hinge).clean(), jack.clean()), name="Motor plate, hinge, jack screw")
motor_plate.material("steel-s235jr", color="#2b2f36")
