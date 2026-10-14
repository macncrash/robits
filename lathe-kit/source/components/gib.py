"""Carriage gib: brass strip in the dovetail on the back (+Y) side, set by three M4 screws."""
from steve import Component
from lathe_shapes import prism_yz
from lathe_params import carriage_x

strip = [(40.1, -98), (42.9, -98), (35.9, -108), (33.1, -108)]
gib = Component("gib", name="Carriage gib (brass)")
gib.add("gib", prism_yz(strip, carriage_x + 2, carriage_x + 68), name="Gib")
gib.material("brass-c36000")
