"""Outer blade flange Ø80 and the left-hand M24 nut (they tighten as the blade cuts)."""
from steve import Component
from coldsaw_shapes import xcyl
from coldsaw_params import blade_y, blade_z

f = xcyl(40, -8, -1, blade_y, blade_z).fuse(xcyl(18, -16, -8, blade_y, blade_z))
f = f.cut(xcyl(12.05, -17, 0, blade_y, blade_z))
outer_flange = Component("outer_flange", name="Outer flange and nut")
outer_flange.add("flange", f.clean(), name="Outer flange")
outer_flange.material("steel-1c45", finish="machined")
