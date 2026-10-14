"""Upper (idler) band wheel, the same as the lower one (its tyre is upper_tyre), on a stub shaft into the tension
slider (two 6204-2RS in the slider). Tracking: the slider's tracking screw tilts the shaft a fraction of a degree."""
from steve import Component
from bandsaw_shapes import wheel
from bandsaw_params import upper_z

centre, _ = wheel(upper_z, 72)
upper_wheel = Component("upper_wheel", name="Upper band wheel (idler)")
upper_wheel.add("centre", centre, name="Wheel centre and shaft")
upper_wheel.material("aluminum-6061-t6", finish="machined")
