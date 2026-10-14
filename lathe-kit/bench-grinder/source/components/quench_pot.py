"""Quench pot (optional): a Ø110 steel cup on a ring bracket clamped round the column at the right, for cooling
work while grinding HSS (never quench carbide)."""
from steve import Component
from grinder_shapes import box, zcyl

px, z0 = 130, 788
bracket = zcyl(57, z0, z0 + 10).cut(zcyl(50.8, z0 - 1, z0 + 11))
bracket = bracket.fuse(box(55, -6, z0, 72, 6, z0 + 10))
bracket = bracket.fuse(zcyl(61, z0, z0 + 10, px).cut(zcyl(56, z0 - 1, z0 + 11, px)))
pot = zcyl(55, z0 - 98, z0 + 10, px).cut(zcyl(53, z0 - 96, z0 + 14, px))
pot = pot.fuse(zcyl(62, z0 + 10, z0 + 13, px).cut(zcyl(53, z0 + 9, z0 + 14, px)))
quench_pot = Component("quench_pot", name="Quench pot")
quench_pot.add("bracket", bracket.clean(), name="Pot bracket")
quench_pot.add("pot", pot.clean(), op="new", name="Pot")
quench_pot.material("steel-s235jr", color="#20242c")
