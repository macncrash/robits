"""Jaw coupling (bought), Ø50 x 60, Ø19 bores both ends, polyurethane spider: drive hub stub to worm input shaft."""
from steve import Component
from coldsaw_shapes import ycyl
from coldsaw_params import gear_x, worm_z

c = ycyl(25, 77, 137, gear_x, worm_z).cut(ycyl(9.5, 76, 102, gear_x, worm_z)).cut(ycyl(9.5, 112, 138, gear_x, worm_z))
coupling = Component("coupling", name="Jaw coupling Ø50 (bought)")
coupling.add("coupling", c.clean(), name="Coupling")
coupling.material("steel-1c45", finish="machined", color="#8a8f96")
