"""AM-02 Rear end bell (spec: cnc/end_bell.md)."""
import numpy as np

from common import *  # noqa: F403
from amdraw import detail, cutting_line, triad, tag

PART = "AM-02-end_bell"
STEP = "end_bell.step"
s = load(STEP)
q = Q(s)

od = q.cyl(103.0)
spig = q.cyl(85.1)
spig_id = q.cyl(60.0)
boss = q.cyl(35.0)
seat = q.cyl(28.0)
groove = q.cyl(29.4)
hole19 = q.cyl(19.0)
cb = q.cyl(8.0, n=4)
th = q.cyl(4.5, n=4)
m3 = q.cyl(2.5, n=3)
m2 = q.cyl(1.6, n=4)
for z in (-48, -46, -36, -33, -38, -36.7):
    q.plane(z)
check(PART, "groove width", groove["z1"] - groove["z0"], 1.3)
check(PART, "groove rear wall from seat floor", groove["z0"] - (-46), 8.0)
check(PART, "seat floor from rear face", -46 - (-48), 2.0)
check(PART, "counterbore depth", cb["z1"] - (-48), 4.5)
check(PART, "M3 drill depth", m3["z1"] - m3["z0"], 9.0, tol=0.6)  # cylinder part ends where the 118° point starts
check(PART, "M2 drill depth", m2["z1"] - m2["z0"], 6.0, tol=0.6)

sh = Sheet("A3")
# ---- rear-face view (from -Z), 1:1
vR = View((0, 0, -1), (-1, 0, 0))
V = PView(sh, vR, (92, 215), 1.0, geo=project(s, vR, hidden=False), label="VIEW FROM REAR (1:1)",
          label_pos=(92, 272))
for r in (46, 37, 24.5):
    V.pcd(r)
V.centreline((60, 0, -48), (-60, 0, -48), ext=0); V.centreline((0, 58, -48), (0, -58, -48), ext=0)
triad(sh, V, (42, 255))
ang = lambda c: np.arctan2(c[1], c[0]) % (2 * np.pi)  # noqa: E731
rows = [["TAG", "X", "Y", "HOLE (from rear face Z -48)", "DEPTH"]]
for i, c in enumerate(sorted(cb["centres"], key=ang)):
    tag(sh, V, (c[0], c[1], -48), f"A{i + 1}", off=(-6 * np.sign(vR.p(c)[0]) * -1, 5 * np.sign(c[1])))
    rows.append([f"A{i + 1}", fmt(c[0], 2), fmt(c[1], 2), "Ø4.5 THRU, cbore Ø8.0 +0.2/0", "cbore 4.5 ±0.1"])
for i, c in enumerate(sorted(m3["centres"], key=ang)):
    tag(sh, V, (c[0], c[1], -48), f"B{i + 1}", off=(0, -4.5))
    rows.append([f"B{i + 1}", fmt(c[0], 2), fmt(c[1], 2), "M3-6H, drill Ø2.5", "8 thd / 9 drill"])
for i, c in enumerate(sorted(m2["centres"], key=ang)):
    tag(sh, V, (c[0], c[1], -48), f"C{i + 1}", off=(0, 4.0))
    rows.append([f"C{i + 1}", fmt(c[0], 2), fmt(c[1], 2), "M2-6H, drill Ø1.6", "5 thd / 6 drill"])
x1, y1 = sh.table(262, 283, [9, 15, 15, 52, 27], rows, h=1.9, row_h=3.7)
y = sh.notes(262, y1 - 4, [
    "X/Y in the STEP frame (Z axis = datum B), seen from the rear.",
    "A, B: position Ø0.2 to B. C (readhead standoffs): position Ø0.05 to B and to the Ø28 seat axis; they set the "
    "encoder alignment (AksIM-2: ±0.4 radial, ±0.3 tangential).",
    "A: ISO 4762 M4×16, head 0.5 below the rear face. B: ISO 7380 M3×25 from the cap, 8 engaged.",
], title=None, width=148, h=1.9, gap=1.1)
cutting_line(sh, V, (56, 0, -48), (-56, 0, -48), "A", look=(0, -1))

# ---- SECTION A-A (plane y = 0, seen from +Y), 2:1, below
vA = View((0, 1, 0), (-1, 0, 0))
cut, loops = section(s, vA, (0, 0, 0))
k = 2.0
CXs = 138
A = PView(sh, vA, (CXs, 110 + 2 * 40.5), k, geo=project(cut, vA, hidden=False), loops=loops,
          label="SECTION A-A (2:1)", label_pos=(CXs, 47), ref=(CXs, 110))
S = lambda x, z: (x, 0, z)  # noqa: E731
A.centreline((0, 0, -50), (0, 0, -31))
for x in (24.5, -24.5):
    A.centreline((x, 0, -49.5), (x, 0, -41), ext=1)
# diameters
dB = sh.dim(A, S(42.55, -33), S(-42.55, -33), "h", pos=22, prefix="Ø", tol="g6 (-0.012/-0.034)", dec=2,
            part=PART, nominal=85.1, label="spigot")
sh.datum(dB[1], (1, 0), "B", L=2)
sh.dim(A, S(30, -33), S(-30, -33), "h", pos=30, prefix="Ø", part=PART, nominal=60)
sh.dim(A, S(17.5, -33), S(-17.5, -33), "h", pos=38, prefix="Ø", part=PART, nominal=35)
d28 = sh.dim(A, S(14, -42), S(-14, -42), "h", pos=-1, prefix="Ø", tol="K7 (+0.006/-0.015)", part=PART, nominal=28,
             ext_a=False, ext_b=False, h=2.3)
sh.dim(A, S(51.5, -48), S(-51.5, -48), "h", pos=-22, prefix="Ø", part=PART, nominal=103)
sh.dim(A, S(9.5, -48), S(-9.5, -48), "h", pos=-30, prefix="Ø", tol="±0.1", part=PART, nominal=19)
fc = sh.fcf(CXs + 30, 66, "coaxiality", "0.015", ["B"], dia=True)
sh.fcf_leader(fc, (CXs + 14, d28[0][1] - 0.2), from_side="left")
sh.rough_leader(A.P(S(-14, -44)), (CXs + 62, 72), "Ra 0.8")
# axial (right side)
sh.dim(A, S(-51.5, -48), S(-51.5, -33), "v", pos=118, part=PART, nominal=15)
sh.dim(A, S(-51.5, -48), S(-51.5, -36), "v", pos=110, part=PART, nominal=12)
# face tolerances
ff = sh.fcf(CXs + 104, 128, "perpendicularity", "0.02", ["B"])
sh.fcf_leader(ff, A.P(S(-47, -36)), from_side="left")
sh.text(ff[0], ff[3] + 1.0, "front face", h=1.8)
fr = sh.fcf(CXs - 104, 82, "flatness", "0.02")
sh.fcf(fr[0], fr[1] - 5, "perpendicularity", "0.02", ["B"])
sh.fcf_leader(fr, A.P(S(46, -48)), from_side="top")
sh.text(fr[0], fr[3] + 1.0, "rear face (standoff seat)", h=1.8)
sh.leader(A.P(S(24.5, -45)), (CXs - 4, 84), ["4× M2-6H, 5 full thread,", "drill Ø1.6 × 6 (C1-C4)"], h=2.0,
          side="left")
sh.leader(A.P(S(-42.8, -33.2)), A.P(S(-42.8, -33.2)) + (14, 14), "0.5×45°", h=2.2)

# ---- DETAIL C (5:1): bearing seat floor, DIN 472 groove, boss
C = detail(sh, A, (15.6, 0, -40.5), 7.6, 5, (318, 162), "C", label_dy=3)
Pz = lambda z: C.P(S(14, z))  # noqa: E731
sh.dim(C, S(14, -46), S(14, -38), "v", pos=-44, tol="+0.05/0", dec=2, part=PART, nominal=8.0,
       label="groove rear wall to seat floor")
sh.dim(C, S(14.7, -38), S(14.7, -36.7), "v", pos=-36, tol="+0.14/0", dec=2, part=PART, nominal=1.3, outside=True,
       tshift=10, label="groove width")
sh.dim(C, S(14, -48), S(14, -46), "v", pos=-36, dec=1, part=PART, nominal=2.0, outside=True, tshift=-8,
       label="seat floor")
sh.leader(C.P(S(14.7, -37.3)), (352, 200), ["DIN 472 28 groove", "Ø29.4 H11 (+0.13/0)"], h=2.1)
sh.leader(C.P(S(14.15, -46)), (352, 128), "relief 0.3 × 0.3", h=2.1)
sh.leader(C.P(S(14.2, -33.2)), (362, 188), "0.5×45° lead-in", h=2.1)

# ---- notes and title block
sh.notes(262, 118, general_notes(STEP, extra=[
    "Material EN AW-6061-T6, with certificate.",
    "Black anodise MIL-A-8625 Type II. MASK: Ø28 seat and its groove, Ø85.10 spigot, tapped holes.",
    "Datum B: spigot axis. Turn the spigot, the Ø28 seat and the groove in one setup (op 10).",
    "Inspect: CMM spigot, seat, groove position and C1-C4 positions; thread gauges.",
]), width=148, h=1.9, gap=1.05)
sh.title_block(fields(PART, "Rear end bell", "1", "EN AW-6061-T6", "Black anodise Type II, fits masked",
                      "2:1 (views as noted)", STEP))
finish(sh, PART)
