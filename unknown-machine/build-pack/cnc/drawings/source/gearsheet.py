"""Shared layout for the gear drawings (AM-13 sun, AM-14 planet, AM-15 ring): end view with the teeth, axial
section of the blank (ISO 2203 conventions: tip line, pitch chain line), and the gear data table."""
import numpy as np

from common import *  # noqa: F403
from amdraw import cutting_line, triad


def gear_views(sh, s, z0, z1, scale, end_c, sec_rx, label_y, plane="x", beyond=True):
    """End view (from +Z) at end_c and SECTION A-A centred at sec_rx: plane x = 0 seen from -X (paper right = +Z,
    up = +Y), or plane y = 0 seen from -Y (up = -X)."""
    vF = View((0, 0, 1), (1, 0, 0))
    F = PView(sh, vF, end_c, scale, geo=project(s, vF, hidden=False), label=f"VIEW FROM FRONT ({int(scale)}:1)",
              label_pos=(end_c[0], label_y))
    zm = (z0 + z1) / 2
    vA = View((-1, 0, 0), (0, 0, 1)) if plane == "x" else View((0, -1, 0), (0, 0, 1))
    cut, loops = section(s, vA, (0, 0, 0))
    A = PView(sh, vA, (sec_rx - scale * zm, end_c[1]), scale, geo=project(cut, vA, hidden=False), loops=loops,
              beyond=beyond,
              label=f"SECTION A-A ({int(scale)}:1)", label_pos=(sec_rx - 8, label_y), ref=(sec_rx, end_c[1]))
    return F, A


def gear_notes(extra=()):
    return [
        "Teeth are hobbed / shaped and ground by the gear shop to the gear data table; the STEP teeth are a "
        "reference shape (ISO 53 profile A with the 0.38 m root fillet), not a machining surface.",
    ] + list(extra)
