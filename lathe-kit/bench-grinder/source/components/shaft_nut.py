"""Shaft nut M20 x 1.5, 30 across flats (right-hand on the right, left-hand on the left). Modelled at x 139..149."""
from steve import Component
from grinder_shapes import hex_x, xcyl

shaft_nut = Component("shaft_nut", name="Shaft nut M20 x 1.5")
shaft_nut.add("nut", hex_x(30, 139, 149).cut(xcyl(10, 138, 150)), name="Nut")
shaft_nut.material("steel-1c60", color="#1d1f22")
