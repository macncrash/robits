"""AM-09 Motor shaft, hollow (spec: cnc/rotor.md part 1)."""
import numpy as np

from common import *  # noqa: F403
from amdraw import detail, cutting_line, triad
from geom import bbox

PART = "AM-09-motor_shaft"
STEP = "rotor.step"
s = load(STEP, solid=lambda ss: max(ss, key=lambda x: bbox(x)[5] - bbox(x)[2]))   # the 120 long body
q = Q(s)

od = q.cyl(12.0)
bore = q.cyl(8.0)
gr = q.cyl(11.5)
flats = q.plane(5.4, normal=(1, 0, 0)), q.plane(-5.4, normal=(1, 0, 0))
for z in (-60, 60, -47.1, -46, -38, -36.9, 47.5):
    q.plane(z)
check(PART, "length", 120.0, 120.0)
check(PART, "across flats", flats[0] - flats[1], 10.8)
check(PART, "groove width", -46 - (-47.1), 1.1)

sh = Sheet("A3")
vM = View((0, -1, 0), (0, 0, 1))     # paper right = +Z (sun end), up = -X: flats edge-on
k = 2.0
M = PView(sh, vM, (200, 195), k, geo=project(s, vM, hidden=True), label="MOTOR SHAFT (2:1)",
          label_pos=(200, 268))
P = lambda x, z: (x, 0, z)  # noqa: E731
M.centreline(P(0, -62), P(0, 62))
U = lambda z, up=6: P(-up, z)  # noqa: E731  point on the upper outline (paper up = -X)
L = lambda z, d=6: P(d, z)     # noqa: E731  lower outline
# overall + bore
sh.dim(M, L(-60), L(60), "h", pos=-64, part=PART, nominal=120, label="length")
sh.dim(M, P(-4, -55), P(4, -55), "v", pos=-131, prefix="Ø", tol="+0.2/0", part=PART, nominal=8, outside=True,
       tshift=-9)
sh.leader(M.P(P(-4, -30)), (100, 252), ["Ø8 +0.2/0 cable bore THRU, straightness 0.1 over 120;",
                                        "drill from both ends (60 each), step ≤0.1 where they meet: deburr"],
          h=1.9, side="right")
# seat zones (all Ø12 nominal): tagged on the view, listed in the zone table
zones = [(-58, -48.5, "g6 (-0.006/-0.017)", "3.2", "encoder hub AM-11 (Loctite 638)"),
         (-46, -38, "k5 (+0.009/+0.001)", "0.4", "6001 inner ring; datum A"),
         (-17, 15.15, "p6 (+0.029/+0.018)", "3.2", "hub sleeve AM-10 press fit"),
         (37, 47, "h6 (0/-0.011)", "0.2", "HK1210 raceway ≥55 HRC, circularity 0.003; datum B"),
         (47.5, 60, "g6 (-0.006/-0.017)", "3.2", "sun AM-13: round portions of the double-D")]
rows = [["ZONE", "FROM REAR END", "Ø12", "Ra", "FUNCTION"]]
for i, (z0, z1, fit, ra, name) in enumerate(zones):
    up = False
    zm = (z0 + z1) / 2 if i != 1 else -43.5
    tip = M.P(L(zm))
    box = tip + (0, -9.5)
    sh.line([tip, box + np.array([0, 2.6])], w=0.25)
    sh.ax.add_patch(__import__("matplotlib").patches.Rectangle(box - (3.2, 2.6), 6.4, 5.2, fill=False, lw=0.7))
    sh.text(box[0], box[1] - 1.1, f"Z{i + 1}", h=2.2, ha="center")
    rows.append([f"Z{i + 1}", f"{fmt(z0 + 60, 2)} - {fmt(z1 + 60, 2)}", fit, ra, name])
sh.table(24, 60, [11, 27, 33, 8, 78], rows, h=1.9, row_h=3.8)
sh.text(24, 33, "Ø12 outside the zones: ISO 2768-m. Zones Z2 and Z4 ground; runout of Z1-Z5 to A-B 0.01.", h=1.8)
sh.dim(M, U(-60), U(-46), "h", pos=24, tol="±0.02", dec=2, part=PART, nominal=14.0, label="groove wall 1 / Z2 start")
sh.dim(M, U(-60), U(-38), "h", pos=32, tol="±0.02", dec=2, part=PART, nominal=22.0, label="groove wall 2 / Z2 end")
sh.dim(M, U(-60), U(-17), "h", pos=40, part=PART, nominal=43, label="Z3 start")
sh.dim(M, U(-17), U(15.15), "h", pos=40, dec=2, part=PART, nominal=32.15, label="Z3 length")
sh.dim(M, L(-60), L(37), "h", pos=-50, part=PART, nominal=97, label="Z4 start")
sh.dim(M, L(37), L(47), "h", pos=-50, part=PART, nominal=10, label="Z4 length")
sh.dim(M, L(47.5), L(60), "h", pos=-40, dec=1, part=PART, nominal=12.5, label="flats / Z5")
sh.dim(M, L(-60), L(-58), "h", pos=-40, part=PART, nominal=2, outside=True, tshift=-8, label="Z1 start")
sh.dim(M, L(-58), L(-48.5), "h", pos=-40, dec=1, part=PART, nominal=9.5, label="Z1 length")
sh.datum(M.P(L(-39.5)) + (0, -0.1), (0, -1), "A", L=40)
sh.datum(M.P(U(42)) + (0, 0.1), (0, 1), "B", L=8)
fr = sh.fcf(234, 122, "circular_runout", "0.01", ["A-B"])
sh.text(fr[2] + 1.5, fr[1] + 1.3, "Z1-Z5", h=1.8)
sh.fcf_leader(fr, M.P(L(-25)), from_side="left")
fh = sh.fcf(274, 122, "circularity", "0.003")
sh.fcf_leader(fh, M.P(L(44)), from_side="top")
sh.text(fh[2] + 1.5, fh[1] + 1.3, "Z4", h=1.8)
# flats
sh.dim(M, P(-5.4, 47.5), P(5.4, 47.5), "v", pos=136, tol="-0.01/-0.03", dec=2, part=PART, nominal=10.8,
       label="across flats")
cutting_line(sh, M, P(-9, 54), P(9, 54), "C", look=(1, 0))

# ---- SECTION C-C through the flats, 5:1
vC = View((0, 0, -1), (0, 1, 0))
cutC, loopsC = section(s, vC, (0, 0, 54))
C = PView(sh, vC, (372, 150), 5.0, loops=loopsC, beyond=False, label="SECTION C-C (5:1)", label_pos=(372, 186))
fsym = sh.fcf(345, 102, "symmetry", "0.02", ["A-B"])
sh.text(345, 98, "flats 10.80 -0.01/-0.03 across, symmetric to A-B", h=1.8)
sh.text(345, 94.5, "within 0.02, parallel to each other 0.01", h=1.8)

# ---- DETAIL D: DIN 471 grooves, 5:1
D = detail(sh, M, P(6, -42), 6.0, 5, (202, 94), "D", label_dy=2)
sh.dim(D, P(6, -47.1), P(6, -46), "h", pos=-12, tol="+0.14/0", dec=2, part=PART, nominal=1.1, outside=True,
       tshift=-12, label="groove width")
sh.leader(D.P(P(5.75, -46.5)), (40, 80), side="right", lines= ["2× DIN 471 12 groove, Ø11.5 h11 (0/-0.11),",
                                            "width 1.10 +0.14/0 (inner walls = 6001 faces)"], h=1.9)

sh.notes(232, 283, general_notes(STEP, extra=[
    "Material 42CrMo4 +QT (AISI 4140 pre-hardened, 28-32 HRC), with certificate. Alternative 16MnCr5 / 8620 "
    "carburised 58-62 HRC, case 0.5-0.8 (model shows 34CrNiMo6 as a stand-in).",
    "Induction-harden the HK1210 raceway (B, z 37-47) to ≥55 HRC, then grind. Journals ground. Ra 0.4 on the 6001 seat (A), Ra 0.2 on the raceway (B).",
    "Black oxide or light oil, except the ground journals.",
    "Ends: 0.5×45° inside and out. Flats (double-D drive for the sun AM-13): z 47.5 to the front end.",
    "Datums A: 6001 seat axis; B: HK1210 raceway axis; A-B common axis.",
], ra="3.2"), width=176, h=1.8, gap=0.95)
sh.title_block(fields(PART, "Motor shaft (hollow)", "1", "42CrMo4 +QT (4140 HT)",
                      "Induction-harden raceway ≥55 HRC, ground; black oxide", "2:1 (views as noted)", STEP))
finish(sh, PART)
