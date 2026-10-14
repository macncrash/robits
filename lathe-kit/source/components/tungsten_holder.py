"""Tungsten holder for the 4-way tool post: 8 x 8 shank in the post's +Y pocket, an L-shaped plate round the
post's front-left corner, and a bored block that holds the electrode at `half_angle` to the disc face, so the flank
lies flat on it and the marks run lengthwise. Bore a sliding fit for 2.4 mm (sleeve it for 1.6 / 3.2); turn the
tungsten by hand between passes and feed with the carriage dial. Modelled with the carriage at rest; in use the
carriage sits 20 mm to the left (carriage_feed 3600), which brings the tip onto the disc face.
"""
import math

import cadquery as cq
from steve import Component
from lathe_shapes import box
from lathe_params import carriage_x, tool_y

half_angle = 15  # deg Half the included point angle (15 = 30 deg point; 22.5 = 45)
tip_y = -28  # mm Where the tip meets the disc (in front of the axis)
reach = 20  # mm Carriage moved left in use
xc = carriage_x + 35
tip_x = 159.0 + 0.05 + reach                          # disc face + 0.05, as modelled at rest
a = math.radians(half_angle)


def along_electrode(shape):
    """Turn a shape built along local +Y (from the tip back) onto the electrode's line through the tip."""
    return shape.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 180 + half_angle).translate(cq.Vector(tip_x, tip_y, 0))


block = along_electrode(box(-4.5, 22, -4.5, 4.5, 50, 4.5))
bore = along_electrode(cq.Solid.makeCylinder(1.25, 60, cq.Vector(0, 10, 0), cq.Vector(0, 1, 0)))
set_screw = along_electrode(cq.Solid.makeCylinder(1.25, 5, cq.Vector(0, 44, 0), cq.Vector(0, 0, 1)))   # M3 drag screw
shank = box(xc - 4, tool_y + 8, -8, xc + 4, tool_y + 18, 0)
plate = box(181, tool_y + 18, -8, xc + 4, tool_y + 26, -4).fuse(box(181, -81, -8, 196, tool_y + 26, -4))
holder = shank.fuse(plate).fuse(block).cut(bore).cut(set_screw)
tungsten_holder = Component("tungsten_holder", name=f"Tungsten holder, {2 * half_angle} deg point")
tungsten_holder.add("holder", holder.clean(), name="Holder")
tungsten_holder.material("aluminum-6061-t6", finish="anodized", color="#8a2b2b")
