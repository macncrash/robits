"""Riser block, 6061: lifts the actuator 70 mm so the Ø250 disc clears the stand top. The pedestal's 4 x M8 go
into tapped holes on top; 4 x M8 counterbored from the top hold the riser to the stand."""
from steve import Component
from sander_shapes import box, zcyl
from sander_params import base_z, riser_h

z0, z1 = base_z - riser_h, base_z
block = box(-70, -72, z0, 70, 28, z1)
for x in (-52, 52):                                  # pedestal bolt pattern (its X ±52, Y 15 / -59), M8 tapped
    for y in (15, -59):
        block = block.cut(zcyl(3.4, z1 - 16, z1, x, y))
for x in (-25, 25):                                  # M8 counterbored into the stand top
    for y in (-45, 5):
        block = block.cut(zcyl(4.5, z0, z1, x, y)).cut(zcyl(7.5, z1 - 30, z1, x, y))
riser = Component("riser", name="Riser block")
riser.add("riser", block.clean(), name="Riser 140 x 100 x 70")
riser.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
