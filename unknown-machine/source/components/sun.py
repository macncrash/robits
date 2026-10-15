"""Sun gear on the motor shaft: a turned blank, teeth hobbed and ground by a gear shop to the data table in
build-pack/cnc/sun.md (the model's teeth are the reference shape, with the 0.38 m root fillet). The bore is a
double-D (Ø12 H7, 10.8 across the flats) matching the flats on the shaft, wire-EDM cut after hardening."""
import cadquery as cq
from steve import Component
from shapes import cyl, box, edge_break
from params import module, sun_teeth, face_width
from gearing import spur_gear

sun = Component("sun", name="Sun gear")
bore = cyl(6, face_width, 0).intersect(box(-5.4, -7, 0, 5.4, 7, face_width))   # double-D: Ø12, 10.8 across flats
gear = spur_gear(module, sun_teeth, face_width).val().cut(bore)
tip_r = module * (sun_teeth / 2 + 1)
for r, z, size, out, up in ((6, 0, 0.5, 1, 1), (6, face_width, 0.5, 1, -1),            # bore lead-ins
                            (tip_r, 0, 0.2, -1, 1), (tip_r, face_width, 0.2, -1, -1)):  # tooth-end tip chamfers
    gear = gear.cut(edge_break(r, z, size, out, up))
sun.add("teeth", gear.translate(cq.Vector(0, 0, 48)), name="Teeth")
sun.material("steel-17crnimo6", finish="machined")   # case-hardening gear steel (18CrNiMo7-6), carburised
