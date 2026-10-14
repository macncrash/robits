"""Spacer tube between the bearing's inner race and the inner wheel flange: the shaft nut clamps nut, outer
flange, wheel, inner flange, spacer and inner race against the shaft shoulder. Under the end bell's lip seal.
Modelled on the right (x 60..111)."""
from steve import Component
from grinder_shapes import xring

spacer = Component("spacer", name="Spacer tube")
spacer.add("spacer", xring(14, 10, 60, 111), name="Spacer")
spacer.material("steel-1c60", finish="polished")
