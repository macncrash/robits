"""Planet gear (modelled at the origin, placed by main.py), with a 10 mm bore for its HK0609 needle bearing."""
from steve import Component
from params import module, planet_teeth, face_width
from gearing import spur_gear

planet = Component("planet", name="Planet gear")
planet.add("teeth", spur_gear(module, planet_teeth, face_width), name="Teeth")
with planet.sketch("pin_hole", on="XY", name="Pin hole") as s:
    s.circle("c1", (0, 0), 5)
planet.extrude("bore", "pin_hole", through_all=True, op="cut", name="Pin bore")
planet.material("steel-17crnimo6", finish="machined")   # case-hardening gear steel (18CrNiMo7-6), carburised
