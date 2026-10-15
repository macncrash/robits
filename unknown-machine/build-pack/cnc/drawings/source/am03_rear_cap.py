"""AM-03 Encoder cap, fluted (spec: cnc/rear_cap.md)."""
import math
import numpy as np

from common import *  # noqa: F403
from amdraw import detail, cutting_line, triad, tag

PART = "AM-03-rear_cap"
STEP = "rear_cap.step"
s = load(STEP)
q = Q(s)

od = q.cyl(84.0)
cav = q.cyl(78.0)
bossd = q.cyl(6.0, n=3)
h34 = q.cyl(3.4, n=3)
h10 = q.cyl(10.0)
h7 = q.cyl(7.0)
for z in (-65, -62, -48):
    q.plane(z)
# flute: flat bottom of the flute on +X (normal X) and its round ends
fl_bottom = q.plane(41.2, normal=(1, 0, 0), tol=0.01)
fl_ends = q.cyl(2.0, axis=(1, 0, 0))
check(PART, "flute depth (radial, from Ø84)", 42.0 - fl_bottom, 1.8, tol=0.01)
zs = sorted(set(round(c[2], 3) for c in fl_ends["centres"]))
check(PART, "flute slot length incl. round ends", zs[-1] - zs[0] + 2.0, 13.5)
check(PART, "flute end from rear face", zs[0] - 1.0 - (-65), 1.5)
check(PART, "cavity depth", -48 - (-62), 14.0)

sh = Sheet("A3")
# ---- view from the front (+Z): into the cavity, 1:1
vF = View((0, 0, 1), (1, 0, 0))
F = PView(sh, vF, (75, 200), 1.0, geo=project(s, vF, hidden=False), label="VIEW FROM FRONT (1:1)",
          label_pos=(75, 252))
F.pcd(37); F.pcd(32)
F.centreline((-47, 0, -48), (47, 0, -48), ext=0); F.centreline((0, -47, -48), (0, 47, -48), ext=0)
triad(sh, F, (28, 262))
cutting_line(sh, F, (0, 47, -48), (0, -47, -48), "A", look=(1, 0))
ang = lambda c: np.arctan2(c[1], c[0]) % (2 * np.pi)  # noqa: E731
rows = [["TAG", "X", "Y", "HOLE", "NOTE"]]
for i, c in enumerate(sorted(h34["centres"], key=ang)):
    tag(sh, F, (c[0], c[1], -48), f"A{i + 1}", off=(6 * np.sign(c[0]), 4 * np.sign(c[1])) if abs(c[0]) > 1 else (8, 0))
    rows.append([f"A{i + 1}", fmt(c[0], 2), fmt(c[1], 2), "Ø3.4 THRU (boss Ø6)", "ISO 273 normal"])
c7 = h7["centres"][0]
tag(sh, F, (c7[0], c7[1], -48), "B1", off=(-1, -6))
rows.append(["B1", fmt(c7[0], 2), fmt(c7[1], 2), "Ø7 +0.2/0 THRU", "cable exit, grommet"])
rows.append(["C1", "0", "0", "Ø10 THRU", "shaft cable hole"])
x1, y1 = sh.table(262, 283, [9, 15, 15, 46, 38], rows, h=1.9, row_h=3.7)
sh.notes(262, y1 - 4, [
    "X/Y in the STEP frame, seen from the front (axis Z).",
    "A1-A3: position Ø0.2 (pattern matches AM-02 holes B1-B3, ISO 7380 M3×25). R1.5 where the bosses meet the "
    "cavity wall (milled with the cavity, Ø6 or smaller end mill).",
    "B1: deburr well; fit a grommet for the Ø6.2 readhead cable.",
], title=None, width=148, h=1.9, gap=1.1)

# ---- SECTION A-A (plane x = 0, seen from +X... arrows look +X), 2:1
vA = View((-1, 0, 0), (0, 0, 1))
cut, loops = section(s, vA, (0, 0, 0))
k = 2.0
A = PView(sh, vA, (185 + 2 * 56.5, 175), k, geo=project(cut, vA, hidden=False), loops=loops,
          label="SECTION A-A (2:1)", label_pos=(185, 278), ref=(185, 175))
Y = lambda y, z: (0, y, z)  # noqa: E731
A.centreline((0, 0, -67), (0, 0, -46))
sh.dim(A, Y(-42, -65), Y(42, -65), "v", pos=-30, prefix="Ø", part=PART, nominal=84)
sh.dim(A, Y(-39, -48), Y(39, -48), "v", pos=30, prefix="Ø", tol="+0.2/0", dec=0, part=PART, nominal=78, text="Ø78 +0.2/0")
sh.dim(A, Y(-5, -62), Y(5, -62), "v", pos=-22, prefix="Ø", part=PART, nominal=10, outside=True, tshift=14)
sh.dim(A, Y(42, -65), Y(42, -48), "h", pos=96, part=PART, nominal=17)
sh.dim(A, Y(-39, -62), Y(-39, -48), "h", pos=-92, tol="+0.2/0", dec=1, part=PART, nominal=14, label="cavity depth")
sh.dim(A, Y(-42, -65), Y(-41.2, -63.5), "h", pos=-101, part=PART, nominal=1.5, outside=True, tshift=-9,
       label="flute end from rear face")
sh.dim(A, Y(-42, -63.5), Y(-41.2, -50), "h", pos=-101, part=PART, nominal=13.5, tshift=3, label="flute length")
ff = sh.fcf(185 + 22, 268 - 16, "flatness", "0.05")
sh.fcf_leader(ff, A.P(Y(41, -48)), from_side="left")
sh.text(ff[2] + 1.5, ff[1] + 1.3, "front face", h=1.8)
sh.leader(A.P(Y(-37, -55)), (150, 70), ["boss Ø6 with Ø3.4 THRU", "(A3 at 270°)"], h=2.0, side="left")

# ---- DETAIL B: flute profile, 5:1
B = detail(sh, A, (0, 41.6, -63), 2.4, 5, (60, 70), "B", label_dy=3)
sh.leader(B.P(Y(41.2, -62.0)), (92, 50), ["48× flutes, pitch 7.5°, one centred on +X", "2.0 +0.1/0 wide, 0.8 deep (model)",
                                           "R1 ends (Ø2 end mill, radial, C-axis)"], h=2.0)

# ---- notes and title block
sh.notes(262, 205, general_notes(STEP, extra=[
    "Material EN AW-6061-T6, with certificate.",
    "Black anodise MIL-A-8625 Type II all over (mask nothing).",
    "Flutes are cosmetic grip: if the look allows, a DIN 82 RAA 1.0 straight knurl on the lathe is acceptable.",
    "Cavity clears the RLS AksIM-2 readhead by about 1.4 mm axially: hold Ø78 and 14.0 to their limits.",
]), width=148, h=1.9, gap=1.05)
sh.title_block(fields(PART, "Encoder cap (fluted)", "1", "EN AW-6061-T6", "Black anodise Type II (all over)",
                      "1:1 (views as noted)", STEP))
finish(sh, PART)
