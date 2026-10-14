"""Chip and coolant tray: 1.5 mm steel rim round the stand top, 40 high, with a drain at the back left
that runs the coolant down to the tank."""
from steve import Component
from coldsaw_shapes import box, zcyl

outer = box(-400, -260, 0, 400, 380, 40)
tray = outer.cut(box(-398.5, -258.5, -1, 398.5, 378.5, 41))
drain = zcyl(10, -60, 0, -300, 280).cut(zcyl(8, -61, 1, -300, 280))
chip_tray = Component("chip_tray", name="Chip and coolant tray")
chip_tray.add("rim", tray.clean(), name="Tray rim")
chip_tray.add("drain", drain.clean(), name="Drain")
chip_tray.material("steel-s235jr", color="#2a2c30")
