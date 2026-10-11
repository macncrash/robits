"""Fixed internal ring gear, pressed into the front flange: the toothed ring seen in the image."""
from steve import Component
from params import module, sun_teeth, planet_teeth, face_width
from gearing import ring_gear as ring_gear_shape

ring_teeth = sun_teeth + 2 * planet_teeth

ring_gear = Component("ring_gear", name="Ring gear")
# Planets with an even tooth count face the ring with a gap, so a ring tooth sits on +X; odd ones, a tooth.
turn = 180 / ring_teeth if planet_teeth % 2 == 0 else 0.0
outer_r = 43
rim = outer_r - (module * ring_teeth / 2 + 1.25 * module)
ring_gear.add("teeth", ring_gear_shape(module, ring_teeth, face_width, rim=rim, turn=turn).translate((0, 0, 48)),
              name="Internal teeth")
ring_gear.material("steel-s235jr", finish="machined", color="#30343c")
