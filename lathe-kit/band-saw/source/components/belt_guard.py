"""Belt guard (1.5 mm steel, machine red): a box behind the lower frame plate round both pulleys and the belt,
open at the front where it meets the plate and the actuator's output, hung from the plate on two tabs."""
from steve import Component
from bandsaw_shapes import box

x0, x1, y0, y1, z0, z1 = -22, 272, 46, 96, -530, -104
shell = box(x0, y0, z0, x1, y1, z1).cut(box(x0 + 3, y0 - 1, z0 + 3, x1 - 3, y1 - 3, z1 - 3))
for x in (x0, x1 - 12):
    shell = shell.fuse(box(x, 42, -140, x + 12, y0 + 1, -110))
belt_guard = Component("belt_guard", name="Belt guard")
belt_guard.add("guard", shell.clean(), name="Belt guard")
belt_guard.material("steel-s235jr", color="#7a2a22")
