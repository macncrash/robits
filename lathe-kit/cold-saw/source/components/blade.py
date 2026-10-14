"""HSS cold-saw blade Ø250 x 2.0, Ø32 bore with two Ø6.2 pin holes on PCD 54, 100 teeth (bought; for steel bar
and tube up to about 70 mm, 200 teeth for thin wall)."""
import math

from steve import Component
from coldsaw_shapes import prism_yz, xcyl
from coldsaw_params import blade_y, blade_z, blade_d, blade_t

r, n = blade_d / 2, 100
pts = []
for k in range(n):
    a0 = 2 * math.pi * k / n
    a1 = 2 * math.pi * (k + 0.75) / n
    pts.append((blade_y + r * math.cos(a0), blade_z + r * math.sin(a0)))
    pts.append((blade_y + (r - 3.5) * math.cos(a1), blade_z + (r - 3.5) * math.sin(a1)))
blade = prism_yz(pts, -blade_t / 2, blade_t / 2)
blade = blade.cut(xcyl(16.05, -2, 2, blade_y, blade_z))
blade = blade.cut(xcyl(3.1, -2, 2, blade_y + 27, blade_z)).cut(xcyl(3.1, -2, 2, blade_y - 27, blade_z))
blade_c = Component("blade", name="HSS cold-saw blade Ø250 (bought)")
blade_c.add("blade", blade.clean(), name="Blade")
blade_c.material("steel-1c60", finish="polished")
