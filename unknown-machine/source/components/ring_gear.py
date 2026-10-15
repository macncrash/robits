"""Fixed internal ring gear, pressed into the front flange: the toothed ring seen in the image.

A turned ring blank, teeth shaped (or wire-EDM cut for prototypes) to the data table in
build-pack/cnc/ring_gear.md; the model's teeth are the reference shape, with the 0.38 m root fillet."""
from steve import Component
from shapes import edge_break
from params import module, sun_teeth, planet_teeth, face_width
from gearing import ring_gear as ring_gear_shape

ring_teeth = sun_teeth + 2 * planet_teeth

ring_gear = Component("ring_gear", name="Ring gear")
# Planets with an even tooth count face the ring with a gap, so a ring tooth sits on +X; odd ones, a tooth.
turn = 180 / ring_teeth if planet_teeth % 2 == 0 else 0.0
outer_r = 43
rim = outer_r - (module * ring_teeth / 2 + 1.25 * module)
shape = ring_gear_shape(module, ring_teeth, face_width, rim=rim, turn=turn).val()
tip_r = module * (ring_teeth / 2 - 1)
for r, z, size, out, up in ((outer_r, 0, 0.5, -1, 1), (outer_r, face_width, 0.5, -1, -1),   # OD press lead-ins
                            (tip_r, 0, 0.2, 1, 1), (tip_r, face_width, 0.2, 1, -1)):        # tooth-end tip chamfers
    shape = shape.cut(edge_break(r, z, size, out, up))
ring_gear.add("teeth", shape.translate((0, 0, 48)), name="Internal teeth")
ring_gear.material("steel-34crnimo6", finish="machined", color="#30343c")   # quenched and tempered (nitriding optional)
