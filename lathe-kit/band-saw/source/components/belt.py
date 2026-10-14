"""Timing belt HTD 1000-8M-30 (125 teeth): 20T to 100T at 238.2 mm centres, 5:1. Drawn as a band over the two
pulleys' outside diameters (teeth not drawn). Tension it by jacking the hinged motor plate."""
import math

from steve import Component
from bandsaw_shapes import prism_xz
from bandsaw_params import lower_z, motor_z

R_pd, r_pd = 254.65 / 2, 50.93 / 2
alpha = math.degrees(math.asin((R_pd - r_pd) / (lower_z - motor_z)))   # tangent angle below horizontal


def outline(R, r, n=120):
    """Belt outline round both pulleys; R and r are pushed out so the chords clear the true circles."""
    R = R / math.cos(math.radians((180 + 2 * alpha) / n / 2))
    r = r / math.cos(math.radians((180 - 2 * alpha) / n / 2))
    pts = []
    for k in range(n + 1):                           # big pulley: over the top, from -alpha to 180 + alpha
        a = math.radians(-alpha + (180 + 2 * alpha) * k / n)
        pts.append((125 + R * math.cos(a), lower_z + R * math.sin(a)))
    for k in range(n + 1):                           # small pulley: under the bottom
        a = math.radians(180 + alpha + (180 - 2 * alpha) * k / n)
        pts.append((125 + r * math.cos(a), motor_z + r * math.sin(a)))
    return pts


outer = prism_xz(outline(R_pd + 2.2, r_pd + 2.2), 55.5, 84.5)
inner = prism_xz(outline(253.28 / 2 + 0.1, 49.56 / 2 + 0.1), 55, 85)
belt = Component("belt", name="Timing belt HTD 1000-8M-30")
belt.add("belt", outer.cut(inner).clean(), name="Belt")
belt.material("pc", color="#16181c")                  # neoprene and glass cord: appearance only
