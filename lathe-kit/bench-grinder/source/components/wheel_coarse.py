"""Grinding wheel Ø150 x 20, A36 (36 grit) for roughing and shaping steel, rated 4140 rpm or more (35 m/s). Bore 20 here (or a 32 bore with the
maker's reducing bush). Modelled on the right (x 115..135); the left one is turned 180 degrees about Z."""
from steve import Component
from grinder_shapes import xring
from grinder_params import wheel_d, wheel_w, wheel_x

wheel_coarse = Component("wheel_coarse", name="Wheel Ø150 x 20 coarse")
wheel_coarse.add("wheel", xring(wheel_d / 2, 10, wheel_x, wheel_x + wheel_w), name="Wheel")
wheel_coarse.material("steel-s235jr", color="#5e6066")   # vitrified abrasive: appearance only, mass about 0.65 kg
