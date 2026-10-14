"""Blade: bi-metal M42, 1829 mm (72 in) x 13 x 0.65, 10/14 TPI for general steel (6 mm for curves, 14/18 TPI for
thin wall). Drawn as a band: the cutting run down through the table at x 0, the return run up at x 250, wrapped
round the top of the upper wheel and the bottom of the lower one; teeth toward the operator (-Y)."""
from steve import Component
from bandsaw_shapes import box, ring_xz
from bandsaw_params import blade_t, blade_w, lower_z, upper_z, wheel_r, wheel_x

w = blade_w / 2
band = box(-blade_t, -w, lower_z, 0, w, upper_z)
band = band.fuse(box(2 * wheel_r, -w, lower_z, 2 * wheel_r + blade_t, w, upper_z))
band = band.fuse(ring_xz(wheel_x, upper_z, wheel_r, wheel_r + blade_t, 0, 180, -w, w))
band = band.fuse(ring_xz(wheel_x, lower_z, wheel_r, wheel_r + blade_t, 180, 360, -w, w))
blade = Component("blade", name="Blade 1829 x 13 x 0.65 bi-metal")
blade.add("blade", band.clean(), name="Blade")
blade.material("steel-1c60", finish="polished", color="#8c9097")
