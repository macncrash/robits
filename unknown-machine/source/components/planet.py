"""Planet gear (modelled at the origin, placed by main.py)."""
from steve import Component
from params import module, planet_teeth, face_width
from gearing import spur_gear

planet = Component("planet", name="Planet gear")
planet.add("teeth", spur_gear(module, planet_teeth, face_width), name="Teeth")
with planet.sketch("pin_hole", on="XY", name="Pin hole") as s:
    s.circle("c1", (0, 0), 3.25)
planet.extrude("bore", "pin_hole", through_all=True, op="cut", name="Pin bore")
planet.material("steel-s235jr", finish="machined")
