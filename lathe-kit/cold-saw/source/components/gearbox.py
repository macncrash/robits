"""Worm gearbox NMRV063 i = 20 (bought; Motovario NMRV-P063 or equal) with a solid input shaft (VS kit), envelope
at catalogue size: 63 mm centre distance, Ø25 hollow output, about 194 N m maximum output torque at this ratio.
Output axis along X through the blade axis; worm along Y above it; Ø19 input shaft out of the back."""
from steve import Component
from coldsaw_shapes import box, xcyl, ycyl
from coldsaw_params import blade_y, blade_z, gear_x, worm_z

case = box(24, -92, 78, 124, 52, 250)
case = case.fuse(ycyl(37, -100, 52, gear_x, worm_z))                            # worm barrel
case = case.fuse(xcyl(36, 124, 128, blade_y, blade_z))                          # output boss, far side
case = case.cut(xcyl(12.5, 19, 129, blade_y, blade_z))                          # Ø25 hollow output
case = case.fuse(ycyl(45, 52, 57, gear_x, worm_z)).fuse(ycyl(9.5, 57, 102, gear_x, worm_z))   # input boss, shaft
gearbox = Component("gearbox", name="Worm gearbox NMRV063 i=20 (bought)")
gearbox.add("gearbox", case.clean(), name="NMRV063")
gearbox.material("aluminum-6061-t6", color="#5b6470")                          # die-cast aluminium case
