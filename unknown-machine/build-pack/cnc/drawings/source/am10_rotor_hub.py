"""AM-10 Rotor hub sleeve (spec: cnc/rotor.md part 2)."""
import numpy as np

from common import *  # noqa: F403
from amdraw import detail
from geom import bbox

PART = "AM-10-rotor_hub"
STEP = "rotor.step"
s = load(STEP, solid=lambda ss: min(ss, key=lambda x: bbox(x)[5] - bbox(x)[2]))   # the 32.15 long body
q = Q(s)
bore = q.cyl(12.0)
seat = q.cyl(30.0)
sh_ = q.cyl(34.0)
for z in (-17, -15, 15.15):
    q.plane(z)
check(PART, "length", 15.15 - (-17), 32.15)
check(PART, "shoulder thickness", 2.0, 2.0)

sh = Sheet("A4")
vA = View((0, -1, 0), (0, 0, 1))
cut, loops = section(s, vA, (0, 0, 0))
k = 2.0
A = PView(sh, vA, (88, 142), k, geo=project(cut, vA, hidden=False), loops=loops, label="SECTION A-A (2:1)",
          label_pos=(88, 192), ref=(88, 142))
P = lambda x, z: (x, 0, z)  # noqa: E731
A.centreline(P(0, -19), P(0, 17))
d12 = sh.dim(A, P(6, 5), P(-6, 5), "v", pos=-50, prefix="Ø", tol="H7 (+0.018/0)", part=PART, nominal=12,
             outside=True, tshift=-22)
sh.datum(d12[1], (0, 1), "A", L=3)
d30 = sh.dim(A, P(15, 10), P(-15, 10), "v", pos=48, prefix="Ø", tol="-0.010/-0.030", dec=3, part=PART, nominal=30)
sh.dim(A, P(17, -16), P(-17, -16), "v", pos=-62, prefix="Ø", part=PART, nominal=34)
sh.dim(A, P(-17, -17), P(-15, 15.15), "h", pos=44, dec=2, part=PART, nominal=32.15, label="length")
sh.dim(A, P(17, -17), P(17, -15), "h", pos=-42, part=PART, nominal=2, outside=True, tshift=-8, label="shoulder")
sh.rough_leader(A.P(P(15, 5)), (150, 120), "Ra 1.6")
fp = sh.fcf(120, 98, "perpendicularity", "0.01", ["A"])
sh.fcf_leader(fp, A.P(P(16, -15)), from_side="left")
sh.text(fp[0], fp[1] - 3.4, "shoulder face (rotor banks here)", h=1.8)
sh.leader(A.P(P(-15.1, 15.0)), (130, 180), "0.5×45° lead-in", h=1.9)
sh.leader(A.P(P(6.1, -17.0)), (58, 98), "0.3×45° both ends", h=1.9, side="left")
D = detail(sh, A, P(-15, -15), 1.6, 10, (215, 150), "B", label_dy=2)
sh.leader(D.P(P(-14.85, -14.6)), (250, 175), ["relief 0.3 × 0.3", "(rotor banks square)"], h=1.9)

sh.notes(22, 86, general_notes(STEP, extra=[
    "Material C45E +N (1.1191), with certificate.",
    "Black oxide; MASK the Ø30 bonding surface.",
    "Press onto the shaft's p6 seat (AM-09 Z3) with Loctite 638. Ø30 gives 0.02-0.04 diametral clearance to the "
    "KBM rotor bore 30.010 for Hysol EA 934NA: Ra 1.6, not polished.",
], threads=False), width=84, h=1.7, gap=0.9)
sh.title_block(fields(PART, "Rotor hub sleeve", "1", "C45E +N (1.1191)", "Black oxide, Ø30 bond face masked",
                      "2:1 (detail 10:1)", STEP))
finish(sh, PART)
