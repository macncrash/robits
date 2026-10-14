"""Headstock plate: the actuator's pedestal bolts on top (4 x M8), the plate bolts to the bed ways (4 x M6)."""
from steve import Component
from lathe_shapes import box, zcyl

headstock_plate = Component("headstock_plate", name="Headstock plate")
plate = box(-40, -70, -98, 90, 70, -88)
for x in (-15, 59):                                  # pedestal base holes (its 4 x M8 clearance) -> M8 tapped here
    for y in (-52, 52):
        plate = plate.cut(zcyl(3.4, -98, -88, x, y))
for x in (-20, 70):                                  # M6 counterbored into the bed ways
    for y in (-25, 25):
        plate = plate.cut(zcyl(3.3, -98, -88, x, y)).cut(zcyl(5.5, -94, -88, x, y))
headstock_plate.add("plate", plate.clean(), name="Plate 130 x 140 x 10")
headstock_plate.material("aluminum-6061-t6", finish="anodized", color="#15171c")
