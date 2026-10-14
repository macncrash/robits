"""Moving lower guard, 2 mm steel: swings about the blade axis. It hangs over the front of the teeth with the
head up and rides up over the work as the head comes down (modelled retracted, at the end of the cut)."""
from steve import Component
from coldsaw_shapes import sector_x
from coldsaw_params import blade_y, blade_z

y, z = blade_y, blade_z
g = sector_x(146, 148, 20, 110, y, z, -22, 18)
g = g.fuse(sector_x(106, 148, 20, 110, y, z, -22, -20)).fuse(sector_x(106, 148, 20, 110, y, z, 16, 18))
lower_guard = Component("lower_guard", name="Lower blade guard")
lower_guard.add("guard", g.clean(), name="Lower guard")
lower_guard.material("steel-s235jr", color="#b8401f")
