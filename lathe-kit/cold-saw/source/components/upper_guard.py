"""Fixed upper blade guard, 2 mm steel, welded: a band and two side plates over the top half of the blade (10 to
185 degrees from the front), bolted to the gearbox's side face by the tab. Coolant line clips to its front."""
from steve import Component
from coldsaw_shapes import box, sector_x
from coldsaw_params import blade_y, blade_z

y, z = blade_y, blade_z
g = sector_x(138, 140, 10, 185, y, z, -18, 14)
g = g.fuse(sector_x(46, 140, 10, 185, y, z, -18, -16)).fuse(sector_x(46, 140, 10, 185, y, z, 12, 14))
g = g.fuse(box(14, y - 15, z + 85, 24, y + 15, z + 100))                       # tab to the gearbox face
upper_guard = Component("upper_guard", name="Upper blade guard")
upper_guard.add("guard", g.clean(), name="Upper guard")
upper_guard.material("steel-s235jr", color="#b8401f")
