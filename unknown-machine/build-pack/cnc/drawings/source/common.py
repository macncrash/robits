"""Shared sheet content for the AM drawing set: general notes, title-block fields, output paths."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, ".."))
PNG = os.environ.get("AM_PNG", os.path.join(__import__("tempfile").gettempdir(), "am_drawings_png"))   # previews
sys.path.insert(0, HERE)

from amdraw import Sheet, PView, DISAGREEMENTS, fmt, check  # noqa: E402,F401
from geom import load, View, project, section, Q  # noqa: E402,F401

DESIGN = "STEVE 02e31a10 rev 48"


def fields(number, title, qty, material, finish, scale, step, part_doc=None):
    return dict(number=number, title=title, qty=qty, material=material, finish=finish, scale=scale,
                source=[part_doc or DESIGN, f"STEP: cnc/step/{step}"])


def general_notes(step, extra=(), ra="3.2", threads=True, edges="-0.3 (break 0.2-0.4 x 45°)"):
    n = [
        "Dimensions in mm. General tolerances ISO 2768-mK. Fits ISO 286-1/-2 (deviations shown in brackets).",
        f"STEP file governs undimensioned geometry: cnc/step/{step} ({DESIGN}).",
        f"Edges ISO 13715 {edges} unless a chamfer is shown. Remove all burrs, especially in bores and holes.",
        f"Surface roughness Ra {ra} µm unless noted (ISO 21920-1).",
    ]
    if threads:
        n.append("Threads ISO metric coarse, 6H internal / 6g external; thread depths are full-thread depths.")
    n.extend(extra)
    return n


def finish(sheet, name, pdf_only=False):
    os.makedirs(PNG, exist_ok=True)
    bad = sheet.overlaps()
    sheet.save(os.path.join(OUT, name + ".pdf"), png=os.path.join(PNG, name + ".png"))
    for b in bad:
        print("  LAYOUT", b)
    for d in DISAGREEMENTS:
        print("  DISAGREE", d)
    return bad


def general_rough(sheet, x, y, ra="3.2", extra=None):
    """General surface texture indication near the title block: Ra x (√ [, Ra y ...])."""
    sheet.rough(x, y, f"Ra {ra}")
    s = "( √ " + (", ".join(extra) if extra else "") + ")"
    sheet.text(x + 22, y + 3.2, s, h=2.5)
