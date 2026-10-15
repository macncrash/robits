"""AM-11 Encoder hub (spec: cnc/encoder_hub.md)."""
import numpy as np

from common import *  # noqa: F403
from amdraw import cutting_line, triad, tag

PART = "AM-11-encoder_hub"
STEP = "encoder_hub.step"
s = load(STEP)
q = Q(s)
bore = q.cyl(12.0)
fl = q.cyl(30.0)
pil = q.cyl(20.0)
col = q.cyl(18.0)
m2 = q.cyl(1.6, n=8)
ss = q.cyl(1.6, axis=(1, 0, 0))
for z in (-48.5, -52.5, -54.3, -58):
    q.plane(z)
check(PART, "flange thickness", 4.0, -48.5 - (-52.5))
check(PART, "pilot length", -52.5 - (-54.3), 1.8)
check(PART, "collar end from flange front face", -48.5 - (-58), 9.5)

sh = Sheet("A3")
# front view: from the flange front face side (+Z), 2:1
vF = View((0, 0, 1), (1, 0, 0))
F = PView(sh, vF, (90, 190), 2.0, geo=project(s, vF, hidden=False), label="VIEW FROM FRONT (2:1)",
          label_pos=(90, 232))
F.pcd(12.5, centre=(0, 0, -48.5))
F.centreline((-17, 0, -48.5), (17, 0, -48.5), ext=0); F.centreline((0, -17, -48.5), (0, 17, -48.5), ext=0)
triad(sh, F, (40, 222))
cutting_line(sh, F, (-18, 0, -48.5), (18, 0, -48.5), "A", look=(0, 1))
ang = lambda c: np.arctan2(c[1], c[0]) % (2 * np.pi)  # noqa: E731
rows = [["TAG", "X", "Y", "HOLE"]]
for i, c in enumerate(sorted(m2["centres"], key=ang)):
    a = ang(c)
    tag(sh, F, (c[0], c[1], -48.5), f"A{i + 1}", off=(7.5 * np.cos(a), 7.5 * np.sin(a)))
    rows.append([f"A{i + 1}", fmt(c[0], 3), fmt(c[1], 3), "M2-6H THRU flange (drill Ø1.6)"])
x1, y1 = sh.table(24, 140, [9, 15, 15, 52], rows, h=1.9, row_h=3.7)
sh.notes(24, y1 - 4, [
    "X/Y in the STEP frame (Z axis = datum G).",
    "A1-A8: position Ø0.05 to G. ISO 7046 M2×6 ring screws, 4 engaged.",
], title=None, width=95, h=1.9, gap=1.05)

# SECTION A-A (plane y = 0, through the set screw at 0°), 4:1: paper right = +Z, up = -X
vA = View((0, -1, 0), (0, 0, 1))
cut, loops = section(s, vA, (0, 0, 0))
k = 4.0
RX, RY = 225, 170
A = PView(sh, vA, (RX + k * 53.25, RY), k, geo=project(cut, vA, hidden=False), loops=loops,
          label="SECTION A-A (4:1)", label_pos=(RX - 20, 254), ref=(RX, RY))
P = lambda x, z: (x, 0, z)  # noqa: E731
A.centreline(P(0, -59.5), P(0, -47))
A.centreline(P(17, -50.5), P(4, -50.5), ext=1)
dG = sh.dim(A, P(6, -50), P(-6, -50), "v", pos=-38, prefix="Ø", tol="H7 (+0.018/0)", part=PART, nominal=12,
            outside=True, tshift=-30)
sh.datum(dG[1], (0, 1), "G", L=3)
d20 = sh.dim(A, P(10, -53.4), P(-10, -53.4), "v", pos=40, prefix="Ø", tol="g6 (-0.007/-0.020)", part=PART,
             nominal=20)
fco = sh.fcf(d20[1][0] + 2, d20[1][1] + 8, "coaxiality", "0.01", ["G"], dia=True)
sh.fcf_leader(fco, (d20[1][0], d20[1][1] - 2), from_side="left")
sh.dim(A, P(15, -49), P(-15, -49), "v", pos=-52, prefix="Ø", part=PART, nominal=30)
sh.dim(A, P(9, -56), P(-9, -56), "v", pos=52, prefix="Ø", tol="0/-0.1", part=PART, nominal=18)
sh.dim(A, P(15, -52.5), P(15, -48.5), "h", pos=-70, tol="±0.02", dec=2, part=PART, nominal=4, label="flange")
sh.dim(A, P(10, -54.3), P(10, -52.5), "h", pos=-70, dec=1, part=PART, nominal=1.8, outside=True, tshift=-10,
       label="pilot")
sh.dim(A, P(9, -58), P(15, -48.5), "h", pos=-80, dec=1, part=PART, nominal=9.5, label="collar end to front face")
sh.datum(A.P(P(-13, -52.5)) + (-0.1, 0), (-1, 0), "H", L=10)
fr = sh.fcf(RX - 70, RY + 52, "circular_runout", "0.01", ["G"])
sh.fcf(fr[0], fr[1] - 5, "flatness", "0.005")
sh.fcf_leader(fr, A.P(P(-12, -52.5)), from_side="right")
sh.text(fr[0], fr[3] + 1.0, "ring mounting face (axial runout)", h=1.8)
fpa = sh.fcf(RX + 14, RY + 66, "parallelism", "0.02", ["H"])
sh.fcf_leader(fpa, A.P(P(-13, -48.5)), from_side="left")
sh.text(fpa[0], fpa[3] + 1.0, "flange front face", h=1.8)
sh.leader(A.P(P(15, -50.5)), (RX + 62, RY - 30), ["M2-6H set screw, radial THRU flange at 0°", "(drill Ø1.6),",
                                                   "DIN 913 M2×3 cup point + Loctite"], h=1.9)
sh.leader(A.P(P(-9.1, -57.7)), (RX + 62, RY + 34), "0.3×45° (all turned edges)", h=1.9)

sh.notes(262, 283, general_notes(STEP, extra=[
    "Material AISI 303 (1.4305): non-magnetic, keep magnetic steel away from the ring's magnet. Passivate "
    "ASTM A967. (Model shows 304.)",
    "Datum G: Ø12 H7 bore; datum H: ring mounting face (flange rear face, carries the RLS MRA039 ring).",
    "Bore goes on the shaft's Ø12 g6 seat (AM-09 Z1) with Loctite 638. Fit with a 0.50 mm shim against the end "
    "bell rear face while it cures (sets the 2.88 ±0.13 ring-to-readhead gap).",
    "Collar Ø18 must pass the readhead's Ø21.2 bore.",
], edges="-0.2 (break 0.1-0.2 x 45°)"), width=148, h=1.9, gap=1.05)
tf = fields(PART, "Encoder hub", "1", "AISI 303 (1.4305)", "Passivate ASTM A967", "4:1 (views as noted)", STEP)
tf["edges"] = "-0.2 (0.1-0.2)"
sh.title_block(tf)
finish(sh, PART)
