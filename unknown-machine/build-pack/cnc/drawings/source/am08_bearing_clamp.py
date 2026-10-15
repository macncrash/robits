"""AM-08 Output-bearing clamp ring (spec: cnc/bearing_clamp.md)."""
import numpy as np

from common import *  # noqa: F403
from amdraw import cutting_line, triad

PART = "AM-08-bearing_clamp"
STEP = "bearing_clamp.step"
s = load(STEP)
q = Q(s)

od = q.cyl(90.0)
lip = q.cyl(54.0)
rim = q.cyl(68.0)
for z in (42.5, 43.5, 45):
    q.plane(z)
check(PART, "overall height", 45 - 42.5, 2.5)
check(PART, "lip thickness", 43.5 - 42.5, 1.0)

sh = Sheet("A4")
vF = View((0, 0, 1), (1, 0, 0))
F = PView(sh, vF, (72, 142), 1.0, geo=project(s, vF, hidden=False), label="VIEW FROM FRONT (1:1)",
          label_pos=(72, 192))
F.centreline((-48, 0, 45), (48, 0, 45), ext=0); F.centreline((0, -48, 45), (0, 48, 45), ext=0)
cutting_line(sh, F, (-48, 0, 45), (48, 0, 45), "A", look=(0, 1))
sh.leader(F.P((19.1, 19.1, 45)), (122, 182), ["Ø54 ±0.05 (lip ID: clears the", "inner ring Ø46 and its seal)"], h=1.9)

vA = View((0, -1, 0), (1, 0, 0))
cut, loops = section(s, vA, (0, 0, 0))
loops = [f for f in loops if f[0][:, 0].mean() > 0]
k = 5.0
X0, Z0 = 133 - k * 27, 140 - k * 43.75
A = PView(sh, vA, (X0, Z0), k, loops=loops, beyond=False, label="SECTION A-A (5:1), one side",
          label_pos=(178, 186), ref=(178, 140))
P = lambda x, z: (x, 0, z)  # noqa: E731
sh.dim(A, P(45, 42.5), P(45, 45), "v", pos=58, tol="+0.03/+0.01", dec=2, part=PART, nominal=2.5,
       label="overall height")
sh.dim(A, P(27, 42.5), P(27, 43.5), "v", pos=-52, dec=1, part=PART, nominal=1.0, outside=True, tshift=-8,
       label="lip")
sh.dim(A, P(27, 45), P(34, 45), "h", pos=24, part=PART, nominal=7, label="lip radial (Ø54 to Ø68)")
sh.dim(A, P(34, 45), P(45, 45), "h", pos=24, part=PART, nominal=11, label="rim radial (Ø68 to Ø90)")
sh.leader(F.P((39.0, -22.5, 45)), (128, 104), "Ø90 g6 (-0.012/-0.034)", h=1.9)
sh.leader(F.P((24.04, -24.04, 45)), (128, 95), ["Ø68 +0.1/0 (rim bore,", "clears the carrier plate Ø66)"], h=1.9)
sh.datum(A.P(P(40, 42.5)), (0, -1), "A", L=5)
ff = sh.fcf(200, 116, "parallelism", "0.01", ["A"])
sh.fcf(ff[0], ff[1] - 5, "flatness", "0.01")
sh.fcf_leader(ff, A.P(P(41.5, 45)), from_side="left")
sh.text(ff[2] + 1.5, ff[1] + 1.3, "top face", h=1.8)
fb = sh.fcf(130, 116, "flatness", "0.01")
sh.fcf_leader(fb, A.P(P(30, 42.5)), from_side="right")
sh.text(fb[0], fb[1] - 3.4, "bottom face (datum A)", h=1.8)
sh.leader(A.P(P(44.85, 44.85)), (236, 152), "0.3×45° (OD both)", h=1.9)
sh.leader(A.P(P(27.1, 43.4)), (150, 140), "0.2×45° (lip both)", h=1.9, side="right")
sh.leader(A.P(P(34.15, 44.85)), (192, 160), "0.3×45°", h=1.9)

sh.notes(22, 86, general_notes(STEP, extra=[
    "Material AISI 303 (1.4305) (the model shows 304). Passivate ASTM A967.",
    "Height sets the crush on the CRBH 3510 outer ring: 0.01-0.04 mm with the flange (AM-04) screwed down. "
    "Check at assembly; lap the top face if there is no gap.",
], threads=False), width=84, h=1.7, gap=0.9, title="NOTES")
sh.title_block(fields(PART, "Output-bearing clamp ring", "1", "AISI 303 (1.4305)", "Passivate ASTM A967",
                      "1:1 (section 5:1)", STEP))
finish(sh, PART)
