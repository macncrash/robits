"""Grinding wheel Ø150 x 20, WA80 (80 grit, white) for HSS tool bits, rated 4140 rpm or more (35 m/s). Bore 20 here (or a 32 bore with the
maker's reducing bush). Modelled on the right (x 115..135); the left one is turned 180 degrees about Z."""
from steve import Component
from grinder_shapes import xring
from grinder_params import wheel_d, wheel_w, wheel_x

wheel_fine = Component("wheel_fine", name="Wheel Ø150 x 20 fine")
wheel_fine.add("wheel", xring(wheel_d / 2, 10, wheel_x, wheel_x + wheel_w), name="Wheel")
wheel_fine.material("steel-s235jr", color="#d9d7cf")   # vitrified abrasive: appearance only, mass about 0.65 kg
