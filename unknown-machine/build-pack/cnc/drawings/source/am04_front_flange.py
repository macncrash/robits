"""AM-04 Front flange (spec: cnc/front_flange.md)."""
import math
import numpy as np

from common import *  # noqa: F403
from amdraw import detail, cutting_line, triad, tag

PART = "AM-04-front_flange"
STEP = "front_flange.step"
s = load(STEP)
q = Q(s)

od = q.cyl(120.0)
bore86 = q.cyl(86.0)
lip = q.cyl(78.0)
rec = q.cyl(90.0)
th = q.cyl(5.5, n=4)
cb = q.cyl(9.5, n=4)
for z in (44, 45, 48, 65):
    q.plane(z)
check(PART, "recess depth", 45 - 44, 1.0)
check(PART, "counterbore depth", 65 - cb["z0"], 6.0)

sh = Sheet("A3")
# ---- front view (+Z), 1:1
vF = View((0, 0, 1), (1, 0, 0))
F = PView(sh, vF, (85, 190), 1.0, geo=project(s, vF, hidden=False), label="VIEW FROM FRONT (1:1)",
          label_pos=(85, 258))
F.pcd(50)
F.centreline((-64, 0, 65), (64, 0, 65), ext=0); F.centreline((0, -64, 65), (0, 64, 65), ext=0)
triad(sh, F, (30, 262))
c45 = np.array([1, 1, 0]) / math.sqrt(2)
cutting_line(sh, F, tuple(c45 * 64 + (0, 0, 65)), tuple(-c45 * 64 + (0, 0, 65)), "A", look=(-1, 1))
ang = lambda c: np.arctan2(c[1], c[0]) % (2 * np.pi)  # noqa: E731
for i, c in enumerate(sorted(th["centres"], key=ang)):
    tag(sh, F, (c[0], c[1], 65), f"A{i + 1}", off=(7 * np.sign(c[0]), -6 * np.sign(c[1])))
sh.leader(F.P((-35.36, -35.36, 65)) + (-3.2, -3.2), (40, 120),
          ["4× Ø5.5 THRU (A1-A4), PCD 100 at 45° + 90°",
           "cbore Ø9.5 +0.2/0 × 5.5 ±0.1 deep (from front face)",
           "position Ø0.2 to C (ISO 4762 M5×30)"], h=2.0, side="right")

# ---- SECTION A-A through A1 / A3 (plane at 45°), 1:1: paper right = +Z, up = the 45° direction
vA = View((-1 / math.sqrt(2), 1 / math.sqrt(2), 0), (0, 0, 1))
cut, loops = section(s, vA, (0, 0, 0))
RX = 205
A = PView(sh, vA, (RX - 54.5, 190), 1.0, geo=project(cut, vA, hidden=False), loops=loops, label="SECTION A-A",
          label_pos=(RX, 276), ref=(RX, 190))
P = lambda r, z: tuple(c45 * r + (0, 0, z))  # noqa: E731   point at radius r (signed) in the section plane
A.centreline(P(0, 41), P(0, 68))
for r in (50, -50):
    A.centreline(P(r, 42), P(r, 67), ext=1)
d90 = sh.dim(A, P(-45, 44), P(45, 44), "v", pos=-22, prefix="Ø", tol="H7 (+0.035/0)", part=PART, nominal=90,
             tshift=-22)
sh.datum(d90[0], (0, -1), "C", L=3)
sh.dim(A, P(-39, 44), P(39, 44), "v", pos=-30, prefix="Ø", part=PART, nominal=78, tshift=24)
sh.dim(A, P(-60, 44), P(60, 44), "v", pos=-38, prefix="Ø", part=PART, nominal=120)
d86 = sh.dim(A, P(-43, 65), P(43, 65), "v", pos=20, prefix="Ø", tol="H7 (+0.035/0)", part=PART, nominal=86)
fc = sh.fcf(d86[1][0] + 2, d86[1][1] + 6, "coaxiality", "0.015", ["C"], dia=True)
sh.fcf_leader(fc, (d86[1][0], d86[1][1] - 3), from_side="left")
sh.rough_leader(A.P(P(43, 56)), (RX + 34, 150), "Ra 0.8")
sh.dim(A, P(60, 44), P(60, 65), "h", pos=72, part=PART, nominal=21)
sh.dim(A, P(43, 48), P(43, 65), "h", pos=64, part=PART, nominal=17, label="ring-gear bore depth")
sh.dim(A, P(-55, 59.5), P(-60, 65), "h", pos=-72, tol="±0.1", dec=1, part=PART, nominal=5.5, outside=True,
       tshift=-10, label="cbore depth (sheet 6.0)")
sh.leader(A.P(P(43.2, 65)), A.P(P(43.2, 65)) + (14, 10), "0.5×45° lead-in", h=2.0)

# ---- DETAIL B (4:1): Ø90 recess, lip, ring-gear seat
B = detail(sh, A, P(-41.5, 46.4), 4.8, 5, (72, 58), "B", label_dy=3)
sh.dim(B, P(-45, 44), P(-45, 45), "h", pos=-28, tol="±0.01", dec=2, part=PART, nominal=1.0, outside=True,
       tshift=-12, label="recess depth")
sh.dim(B, P(-43, 44), P(-43, 48), "h", pos=-36, part=PART, nominal=4, label="lip", tshift=-14, outside=True)
sh.leader(B.P(P(-43.15, 48)), (112, 40), ["relief 0.3 × 0.3", "at the ring-gear seat"], h=2.0)
sh.leader(B.P(P(-45.15, 44.15)), (112, 70), "0.3×45°", h=2.0)
fp = sh.fcf(112, 54, "perpendicularity", "0.02", ["C"])
sh.fcf_leader(fp, B.P(P(-40.5, 48)), from_side="left")
sh.text(fp[0], fp[3] + 1.0, "lip face (ring-gear seat), datum D", h=1.8)
sh.datum(B.P(P(-40.0, 48)), (1, 0), "D", L=16)
fr = sh.fcf(160, 30, "flatness", "0.02")
sh.fcf(fr[0], fr[1] - 5, "parallelism", "0.02", ["D"])
sh.fcf_leader(fr, A.P(P(-52, 44)), from_side="top")
sh.text(fr[2] + 1.5, fr[1] + 1.2, "rear face (on the housing)", h=1.8)

sh.notes(262, 283, general_notes(STEP, extra=[
    "Material EN AW-6061-T6, with certificate.",
    "Black anodise MIL-A-8625 Type II. MASK: Ø86 ring-gear bore, Ø90 recess, rear face.",
    "Datum C: Ø90 recess axis. Turn Ø86 and Ø90 in one setup if possible, or hold the part on C for op 20.",
    "Ring gear (AM-15) is pressed in from the front with Loctite 638, against the lip (D). Clamp-ring crush: with "
    "the flange screwed down the recess floor presses the clamp ring (AM-08) 0.01-0.04 mm onto the bearing.",
]), width=148, h=1.9, gap=1.05)
sh.title_block(fields(PART, "Front flange", "1", "EN AW-6061-T6", "Black anodise Type II, fits masked",
                      "1:1 (views as noted)", STEP))
finish(sh, PART)
