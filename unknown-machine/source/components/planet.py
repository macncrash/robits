"""Planet gear (modelled at the origin, placed by main.py), with a 10 mm bore for its HK0609 needle bearing.

A turned blank, teeth hobbed and ground by a gear shop to the data table in build-pack/cnc/planet.md (the model's
teeth are the reference shape, with the 0.38 m root fillet)."""
from steve import Component
from shapes import edge_break
from params import module, planet_teeth, face_width
from gearing import spur_gear

planet = Component("planet", name="Planet gear")
planet.add("teeth", spur_gear(module, planet_teeth, face_width), name="Teeth")
with planet.sketch("pin_hole", on="XY", name="Pin hole") as s:
    s.circle("c1", (0, 0), 5)
planet.extrude("bore", "pin_hole", through_all=True, op="cut", name="Pin bore")
tip_r = module * (planet_teeth / 2 + 1)
for k, (r, z, size, out, up) in enumerate(((5, 0, 0.3, 1, 1), (5, face_width, 0.3, 1, -1),          # bore lead-ins (drawn cup)
                                           (tip_r, 0, 0.2, -1, 1), (tip_r, face_width, 0.2, -1, -1))):  # tip chamfers
    planet.add(f"break_{k + 1}", edge_break(r, z, size, out, up), op="cut", name=f"Edge break {k + 1}")
planet.material("steel-17crnimo6", finish="machined")   # case-hardening gear steel (18CrNiMo7-6), carburised
