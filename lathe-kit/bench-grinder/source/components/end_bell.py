"""End bell (two, the left one turned 180 degrees about Z): 6061, carries a 6204-2RS bearing in a Ø47 pocket
against its outer shoulder, 4 x M5 clearance into the barrel, 3 x M5 tapped on its face for the wheel guard.
Modelled on the right (x 40..62)."""
import math
from steve import Component
from grinder_shapes import xcyl
from grinder_params import spindle_z

body = xcyl(54, 40, 62).cut(xcyl(23.5, 39, 60)).cut(xcyl(15, 59, 63))
for a in (45, 135, 225, 315):
    y, z = 48 * math.cos(math.radians(a)), spindle_z + 48 * math.sin(math.radians(a))
    body = body.cut(xcyl(2.75, 39, 63, y, z)).cut(xcyl(4.5, 56, 63, y, z))
for a in (90, 210, 330):
    y, z = 34 * math.cos(math.radians(a)), spindle_z + 34 * math.sin(math.radians(a))
    body = body.cut(xcyl(2.1, 50, 63, y, z))
end_bell = Component("end_bell", name="End bell")
end_bell.add("end_bell", body.clean(), name="End bell")
end_bell.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
