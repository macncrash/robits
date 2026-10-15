"""AM-01 Motor housing (spec: cnc/housing.md)."""
import numpy as np

from common import *  # noqa: F403
from amdraw import detail, cutting_line, view_arrow

PART = "AM-01-housing"
STEP = "housing.step"
s = load(STEP)
q = Q(s)

# ---- features, from the model (each lookup fails if the model lacks it)
bore = q.cyl(85.1, z=0)                 # stator bore, datum A
groove = q.cyl(85.5)                    # adhesive grooves
ledge = q.cyl(81.0)
seat = q.cyl(60.0)
cbore = q.cyl(90.0, z=43)
bulk = q.cyl(48.0)
front = q.cyl(120.0)
fins = q.cyl(96.0)
rear = q.cyl(103.0)
fin_root = q.cyl(90.0, z=-21.5)
m5ax = q.cyl(4.2, n=4, axis=(0, 0, 1))
m4 = q.cyl(3.3, n=4, axis=(0, 0, 1))
m5rad = q.cyl(4.2, axis=(0, 1, 0), n=4)
dowel = q.cyl(4.0, axis=(0, 1, 0), n=2)
z_rear, z_front = q.plane(-36), q.plane(44)
z_ledge, z_floor, z_cb = q.plane(29), q.plane(32.5), q.plane(42.4)
check(PART, "seat floor below front face", z_front - z_floor, 11.5)
check(PART, "Ø90 counterbore depth", z_front - z_cb, 1.6)
check(PART, "stator bore Ø", bore["d"], 85.1)
check(PART, "groove Ø", groove["d"], 85.5)

sh = Sheet("A3")
# ---- main view: SECTION A-A, plane x = 0, seen from -X; paper right = +Z (output), up = +Y (away from pedestal)
vA = View((-1, 0, 0), (0, 0, 1))
cut, loops = section(s, vA, (0, 0, 0))
CX, CY = 165, 170
A = PView(sh, vA, (CX, CY), 1.0, geo=project(cut, vA, hidden=False), loops=loops, label="SECTION A-A",
          label_pos=(CX + 4, 270))
A.centreline((0, 0, -40), (0, 0, 48))
R = lambda y, z: (0, y, z)  # noqa: E731  model point in the section plane

# diameters, rear side (left of the view)
sh.dim(A, R(-51.5, -36), R(51.5, -36), "v", pos=-36 - 9, prefix="Ø", part=PART, nominal=103)
sh.dim(A, R(-48, -24), R(48, -24), "v", pos=-36 - 17, prefix="Ø", tol="g6 (-0.012/-0.034)", part=PART,
       nominal=96, tshift=-18)
bA = sh.dim(A, R(-42.55, -36), R(42.55, -36), "v", pos=-36 - 26, prefix="Ø", tol="+0.035/0", dec=3, part=PART,
            nominal=85.1, tshift=18, label="stator bore")
sh.datum(bA[0], (0, -1), "A", L=3)
f = sh.fcf(bA[0][0] - 1, bA[0][1] - 20, "cylindricity", "0.02", anchor="right")
sh.fcf_leader(f, (bA[0][0], bA[0][1] - 12), from_side="right")
# front side (right of the view)
sh.dim(A, R(-24, 33), R(24, 33), "v", pos=44 + 7, prefix="Ø", part=PART, nominal=48)
bB = sh.dim(A, R(-30, 40), R(30, 40), "v", pos=44 + 15, prefix="Ø", tol="H7 (+0.030/0)", part=PART, nominal=60)
sh.dim(A, R(-40.5, 30), R(40.5, 30), "v", pos=44 + 23, prefix="Ø", tol="±0.1", part=PART, nominal=81, tshift=22)
bC = sh.dim(A, R(-45, 44), R(45, 44), "v", pos=44 + 31, prefix="Ø", tol="H7 (+0.035/0)", part=PART, nominal=90)
bD = sh.dim(A, R(-60, 20), R(60, 20), "v", pos=44 + 39, prefix="Ø", tol="g6 (-0.012/-0.034)", part=PART,
            nominal=120)
sh.datum(bB[0], (0, -1), "B", L=3)
fr = sh.fcf(bB[0][0] + 1, bB[0][1] - 26, "circular_runout", "0.015", ["A"], anchor="right")
sh.fcf_leader(fr, (bB[0][0], bB[0][1] - 9), from_side="top")
fc = sh.fcf(252, 186, "coaxiality", "0.015", ["B"], dia=True)
sh.fcf_leader(fc, (bC[1][0], 189), from_side="left")


# axial dimensions (above)
top = 60
sh.dim(A, R(60, -36), R(60, 44), "h", pos=top + 26, part=PART, nominal=80, label="overall length")
sh.dim(A, R(60, 14), R(60, 44), "h", pos=top + 10, part=PART, nominal=30)
sh.dim(A, R(51.5, -36), R(51.5, -26), "h", pos=top + 10, part=PART, nominal=10)
sh.dim(A, R(42.55, -36), R(40.5, 29), "h", pos=top + 18, part=PART, nominal=65, label="bore length to ledge")
# axial dimensions (below)
bot = -60
sh.dim(A, R(-30, 32.5), R(-60, 44), "h", pos=bot - 9, tol="0/-0.02", dec=2, part=PART, nominal=11.5,
       label="seat floor depth", tshift=-14, outside=True)
sh.dim(A, R(-42.55, 29), R(-60, 44), "h", pos=bot - 17, part=PART, nominal=15)
for zz in (22, 40):
    A.centreline((0, -61, zz), (0, -50, zz), ext=2)
sh.dim(A, R(-61, 22), R(-61, 40), "h", pos=bot - 25, tol="±0.01", dec=2, part=PART, nominal=18, label="dowel pitch")
sh.dim(A, R(-61, 40), R(-60, 44), "h", pos=bot - 25, part=PART, nominal=4, tshift=7, outside=True)


# perpendicularity / flatness / runout of faces
fp = sh.fcf(A.c[0] - 25, A.c[1] + top + 31, "perpendicularity", "0.03", ["A"], anchor="right")
sh.fcf_leader(fp, A.P(R(41.5, 29)) + (0, 0.3), from_side="right")
sh.text(fp[0], fp[3] + 1.0, "ledge face", h=1.8)
ff = sh.fcf(A.c[0] + 52, A.c[1] + top + 31, "perpendicularity", "0.02", ["A"])
sh.fcf_leader(ff, A.P(R(56, 44)), from_side="bottom")
sh.fcf(ff[0], ff[3], "flatness", "0.02")
sh.text(ff[0], ff[3] + 6.2, "front face", h=1.8)
fs_ = sh.fcf(A.c[0] + 52, A.c[1] + top + 13, "circular_runout", "0.015", ["A"])
sh.fcf_leader(fs_, A.P(R(27, 32.5)) + (0.3, 0), from_side="bottom")
sh.text(fs_[2] + 1.5, fs_[1] + 1.2, "seat floor", h=1.8)

# roughness
sh.rough_leader(A.P(R(42.55, -10)), A.P(R(42.55, -10)) + (16, -24), "Ra 1.6")


# chamfer callouts


# fin grooves
sh.leader(A.P(R(-46.5, -10.4)), (118, 94),
          ["8× fin grooves 2.5 wide to Ø90,", "pitch 40/9 = 4.44 from the rear", "end of the fins (z -26)"],
          side="left", h=2.2)

# ---- VIEW B: from the front (+Z), 1:2
vB = View((0, 0, 1), (1, 0, 0))
B = PView(sh, vB, (60, 220), 0.5, geo=project(s, vB, hidden=False), label="VIEW B (1:2)", label_pos=(60, 266))
cutting_line(sh, B, (0, 63, 44), (0, -63, 44), "A", look=(-1, 0))
B.pcd(50)
for c in m5ax["centres"]:
    B.centremark((c[0], c[1], 44), 2.1, ext=1)
view_arrow(sh, A.P(R(70, 47)), (-1, 0), "B")
# ---- VIEW C: from the rear (-Z), 1:2
vC = View((0, 0, -1), (-1, 0, 0))
C = PView(sh, vC, (60, 133), 0.5, geo=project(s, vC, hidden=False), label="VIEW C (1:2)", label_pos=(60, 174))
C.pcd(46)
for c in m4["centres"]:
    C.centremark((c[0], c[1], -36), 1.65, ext=1)
view_arrow(sh, A.P(R(66, -39)), (1, 0), "C")
# ---- VIEW D: from below (-Y), 1:2
vD = View((0, -1, 0), (0, 0, 1))
D = PView(sh, vD, (160, 44), 0.5, geo=project(s, vD, hidden=False), label="VIEW D (1:2)", label_pos=(160, 77))
view_arrow(sh, A.P(R(-62, 9)), (0, 1), "D")

def tag(pv, pt, name, off=(3.5, 3.5)):
    P = pv.P(pt)
    sh.text(P[0] + off[0], P[1] + off[1], name, h=2.0, ha="center", va="center", check=False)

ang = lambda c: np.arctan2(c[1], c[0]) % (2 * np.pi)  # noqa: E731
rows = [["TAG", "X", "Y", "Z", "HOLE", "THREAD / DRILL", "FROM"]]
for i, c in enumerate(sorted(m5ax["centres"], key=ang)):
    tag(B, (c[0], c[1], 44), f"A{i + 1}", off=(4.5 * np.sign(c[0]), 3.2 * np.sign(c[1])))
    rows.append([f"A{i + 1}", fmt(c[0], 2), fmt(c[1], 2), "44", "M5-6H", "15 / Ø4.2×18", "front face"])
for i, c in enumerate(sorted(m4["centres"], key=ang)):
    tag(C, (c[0], c[1], -36), f"B{i + 1}", off=(-4.5 * np.sign(c[0]), 3.2 * np.sign(c[1])))
    rows.append([f"B{i + 1}", fmt(c[0], 2), fmt(c[1], 2), "-36", "M4-6H", "9 / Ø3.3×10.5", "rear face"])
for i, c in enumerate(sorted(m5rad["centres"], key=lambda c: (c[2], c[0]))):
    tag(D, (c[0], -60, c[2]), f"C{i + 1}", off=(-4.2 if c[2] < 30 else 4.2, 0))
    rows.append([f"C{i + 1}", fmt(c[0], 2), "-57.83", fmt(c[2], 2), "M5-6H", "12 / Ø4.2 to Y-43.5", "Ø120 (spot)"])
for i, c in enumerate(sorted(dowel["centres"], key=lambda c: c[2])):
    tag(D, (0, -60, c[2]), f"D{i + 1}", off=(-4.2 if c[2] < 30 else 4.2, 0))
    rows.append([f"D{i + 1}", "0", "-60", fmt(c[2], 2), "Ø4 H7", "6 min / Ø4×8", "Ø120"])
x1, y1 = sh.table(262, 283, [8, 13, 13, 11, 14, 33, 17], rows, h=1.9, row_h=3.7)
sh.notes(262, y1 - 4, [
    "Coordinates in the STEP frame: Z axis = datum A, Z0 as the model (front face Z 44, rear face Z -36).",
    "Position Ø0.2 to A for A1-A4, B1-B4, C1-C4. D1-D2: Ø4 H7 (+0.012/0), position Ø0.02 to A and to each other (±0.01), dowels ISO 8734 4 m6 slip here.",
    "C1-C4 enter the Ø120 at 15.5°: spot face with a Ø5 flat end mill before drilling.",
], title=None, width=148, h=1.9, gap=1.1)

# ---- details
E = detail(sh, A, (0, 42.7, -23.5), 2.8, 10, (52, 42), "E")
sh.dim(E, R(42.75, -26), R(42.75, -21), "h", pos=-6, part=PART, nominal=5, text="5.0")
sh.leader(E.P(R(42.65, -22)), (86, 64),
          ["6× adhesive grooves 5.0 wide,", "0.20 ±0.05 deep (Ø85.50 ±0.10),", "pitch 9.00, from z -26 to 24",
           "(first groove 10.0 from rear face)"], h=2.0)
F = detail(sh, A, (0, 37.5, 37), 8.5, 2, (207, 42), "F", label_dy=9)
sh.text(207, 18, "corner reliefs 0.3 × 0.3", h=2.0, ha="center")
sh.leader(F.P(R(30.15, 32.5)), (199, 21.5), "", h=2.0, side="left", shoulder=0.01)
sh.leader(F.P(R(42.7, 29)), (196, 21.5), "", h=2.0, side="left", shoulder=0.01)
sh.dim(F, R(45.2, 42.4), R(45.2, 44), "h", pos=20, tol="±0.02", dec=2, part=PART, nominal=1.6, outside=True,
       tshift=-9, label="cbore depth")

# ---- notes and title block
sh.notes(300, 200, general_notes(STEP, extra=[
    "Material EN AW-6061-T6 (T6511 extruded bar acceptable), with certificate.",
    "Black anodise MIL-A-8625 Type II Class 2, 8-12 µm. MASK (chromate MIL-DTL-5541 Type II Class 3 instead): "
    "Ø85.100 bore and grooves, Ø60 seat and floor, Ø90 counterbore, Ø120 and Ø96, tapped holes (or chase after "
    "anodising), dowel holes. Fits apply after finishing.",
    "Turn Ø60, its floor and Ø90 in one setup. Ø60 seat and its floor Ra 0.8. Stator bore Ra 1.6 (not polished: bonded joint).",
    "Chamfers 0.5×45°: stator-bore entry (rear), Ø60 seat entry, Ø120 front edge, Ø120/Ø96 step, Ø103 rear edge.",
    "Inspect: CMM bores and runouts to A, front-face flatness, hole positions; groove depth by gauge or replica; "
    "thread gauges after anodise; dowels (AM-05) must drop in and lift off freely.",
]), width=110, h=1.9, gap=1.05)
general_rough(sh, 340, 81, "3.2", ["Ra 1.6", "Ra 0.8"])
sh.title_block(fields(PART, "Motor housing", "1", "EN AW-6061-T6", "Black anodise Type II, fits masked (chromate)",
                      "1:1 (views as noted)", STEP))
finish(sh, PART)
