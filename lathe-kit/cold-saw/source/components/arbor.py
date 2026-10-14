"""Blade arbor, 42CrMo4: Ø25 keyed through the gearbox's hollow output, a collar against its face, the inner blade
flange (Ø80) and the Ø32 blade seat with two drive pins; M24 left-hand nose for the outer flange and nut."""
from steve import Component
from coldsaw_shapes import xcyl
from coldsaw_params import blade_y, blade_z

y, z = blade_y, blade_z
arbor = xcyl(12.5, 24, 128, y, z).fuse(xcyl(22, 8, 24, y, z)).fuse(xcyl(40, 1, 8, y, z))
arbor = arbor.fuse(xcyl(16, -1, 1, y, z)).fuse(xcyl(12, -16, -1, y, z))
arbor = arbor.fuse(xcyl(3, -1, 1, y + 27, z)).fuse(xcyl(3, -1, 1, y - 27, z))       # drive pins
arbor_c = Component("arbor", name="Blade arbor")
arbor_c.add("arbor", arbor.clean(), name="Arbor")
arbor_c.material("steel-34crnimo6", finish="machined", color="#4a4d52")
