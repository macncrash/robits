"""Lower (driven) band wheel, Ø250 over its urethane tyre (the separate component lower_tyre): cast 6061 centre on a
Ø20 shaft through the frame's bearing boss (two 6204-2RS) to the 100T pulley behind. Turns at up to 212 rpm (166
m/min blade speed)."""
from steve import Component
from bandsaw_shapes import wheel
from bandsaw_params import lower_z

centre, _ = wheel(lower_z, 88)
lower_wheel = Component("lower_wheel", name="Lower band wheel (driven)")
lower_wheel.add("centre", centre, name="Wheel centre and shaft")
lower_wheel.material("aluminum-6061-t6", finish="machined")
