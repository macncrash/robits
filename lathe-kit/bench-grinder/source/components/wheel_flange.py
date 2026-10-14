"""Wheel flange Ø60 (at least a third of the wheel, as EN 12413 asks), relieved in the middle so it clamps on its
rim; use the wheel's blotters between flange and wheel. Modelled as the right inner flange (x 111..115)."""
from steve import Component
from grinder_shapes import xring

flange = xring(30, 10, 111, 115).cut(xring(22, 14, 114, 116))
wheel_flange = Component("wheel_flange", name="Wheel flange Ø60")
wheel_flange.add("flange", flange.clean(), name="Flange")
wheel_flange.material("steel-1c60", finish="machined")
