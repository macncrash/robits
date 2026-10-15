"""AM-07 Planet carrier, front disk + output hub (spec: cnc/carrier_disk.md). STEVE part d93731cc rev 5."""
import numpy as np

from common import *  # noqa: F403
from amdraw import detail, cutting_line, triad, tag

PART = "AM-07-carrier_disk"
STEP = "carrier_disk.step"
s = load(STEP)
q = Q(s)

disk = q.cyl(66.0)
hub = q.cyl(20.0)
bore = q.cyl(8.0)
pins = q.cyl(6.0, n=3)
clr = q.cyl(4.5, n=3)
m4 = q.cyl(3.3, n=6)
for z in (60.5, 65.5, 72, 62.5):
    q.plane(z)
check(PART, "pin hole depth", pins["z1"] - pins["z0"], 2.0)
csk = [c for c in q.cones()]
assert csk and all(abs(c["half_angle"] - 45) < 0.01 for c in csk[:3]), csk[:3]

sh = Sheet("A3")
vF = View((0, 0, 1), (1, 0, 0))
F = PView(sh, vF, (96, 206), 2.0, geo=project(s, vF, hidden=False), label="VIEW FROM FRONT (2:1)",
          label_pos=(96, 276))
F.pcd(22.5, centre=(0, 0, 65.5)); F.pcd(25, centre=(0, 0, 65.5))
F.centreline((-35, 0, 72), (35, 0, 72), ext=0); F.centreline((0, -35, 72), (0, 35, 72), ext=0)
triad(sh, F, (30, 270))
cutting_line(sh, F, (-34.5, 0, 72), (34.5, 0, 72), "A", look=(0, 1))
ang = lambda c: np.arctan2(c[1], c[0]) % (2 * np.pi)  # noqa: E731
rows = [["TAG", "X", "Y", "HOLE", "DEPTH / NOTE"]]
for i, c in enumerate(sorted(pins["centres"], key=ang)):
    a = ang(c)
    tag(sh, F, (c[0], c[1], 72), f"A{i + 1}", off=(9 * np.cos(a + 0.5), 9 * np.sin(a + 0.5)))
    rows.append([f"A{i + 1}", fmt(c[0], 3), fmt(c[1], 3), "Ø6 H7 (+0.012/0), from back face", "2.0 +0.1/0, flat"])
for i, c in enumerate(sorted(clr["centres"], key=ang)):
    a = ang(c)
    tag(sh, F, (c[0], c[1], 72), f"B{i + 1}", off=(9 * np.cos(a + 0.45), 9 * np.sin(a + 0.45)))
    rows.append([f"B{i + 1}", fmt(c[0], 3), fmt(c[1], 3), "Ø4.5 THRU, csk 90° Ø9.0-9.2 (front)", "ISO 10642 M4"])
for i, c in enumerate(sorted(m4["centres"], key=ang)):
    a = ang(c)
    tag(sh, F, (c[0], c[1], 72), f"C{i + 1}", off=(5.5 * np.cos(a), 5.5 * np.sin(a)))
    rows.append([f"C{i + 1}", fmt(c[0], 3), fmt(c[1], 3), "M4-6H THRU (drill Ø3.3)", "arm load holes"])
x1, y1 = sh.table(24, 128, [9, 15, 15, 58, 30], rows, h=1.8, row_h=3.5)
sh.notes(24, y1 - 4, [
    "X/Y in the STEP frame (Z axis = output axis).",
    "A1-A3: co-drill with AM-06 clamped on, then ream Ø6 H7 here (slip on the pins); end-mill flat bottoms. "
    "They form datum F (the pin-hole pattern, R22.5).",
    "B1-B3: ISO 10642 M4 head (Ø8.96 max) flush to 0.2 below the front face. C1-C6: position Ø0.1 to G.",
], title=None, width=127, h=1.8, gap=1.0)

vA = View((0, -1, 0), (0, 0, 1))
cut, loops = section(s, vA, (0, 0, 0))
RX, RY = 236, 192
A = PView(sh, vA, (RX - 2 * 66.25, RY), 2.0, geo=project(cut, vA, hidden=False), loops=loops,
          label="SECTION A-A (2:1)", label_pos=(RX, 276), ref=(RX, RY))
P = lambda x, z: (x, 0, z)  # noqa: E731
A.centreline(P(0, 58.5), P(0, 74))
A.centreline(P(22.5, 59), P(22.5, 63.5), ext=1); A.centreline(P(-22.5, 59), P(-22.5, 67), ext=1)
d20 = sh.dim(A, P(10, 70), P(-10, 70), "v", pos=26, prefix="Ø", tol="g6 (-0.007/-0.020)", part=PART, nominal=20)
sh.datum(d20[1], (0, 1), "G", L=3)
fco = sh.fcf(d20[0][0] + 2, d20[0][1] - 20, "coaxiality", "0.01", ["F"], dia=True)
sh.fcf_leader(fco, (d20[0][0], d20[0][1] - 4), from_side="left")
sh.dim(A, P(4, 72), P(-4, 72), "v", pos=40, prefix="Ø", tol="+0.1/0", part=PART, nominal=8, outside=True,
       tshift=-12)
sh.dim(A, P(33, 60.5), P(-33, 60.5), "v", pos=-30, prefix="Ø", part=PART, nominal=66)
sh.dim(A, P(-33, 60.5), P(-10, 72), "h", pos=78, part=PART, nominal=11.5, label="overall length")
sh.dim(A, P(-33, 60.5), P(-33, 65.5), "h", pos=70, part=PART, nominal=5, label="disk")
sh.datum(A.P(P(31, 60.5)), (-1, 0), "E", L=6)
fe = sh.fcf(RX - 70, RY - 60, "flatness", "0.01")
sh.fcf_leader(fe, A.P(P(28, 60.5)), from_side="right")
sh.text(fe[0], fe[1] - 3.4, "back face (on the posts)", h=1.8)
fp = sh.fcf(RX + 18, RY - 56, "parallelism", "0.01", ["E"])
sh.fcf_leader(fp, A.P(P(30, 65.5)), from_side="left")
sh.text(fp[0], fp[1] - 3.4, "front (output) face", h=1.8)
sh.leader(A.P(P(22.5 + 3, 61.5)), (RX + 30, RY - 32), ["3× Ø6 H7, 2.0 +0.1/0 deep (A1-A3)"], h=1.9)
sh.leader(A.P(P(-22.5 - 3.4, 64.6)), (RX + 22, RY + 52), ["3× Ø4.5 THRU, csk 90° × Ø9.0-9.2 (B1-B3)"], h=1.9)
sh.leader(A.P(P(-10.3, 65.8)), (RX + 34, RY + 30), ["relief 0.3 × 0.3 at the pilot root,", "0.5×45° pilot lead-in"],
          h=1.9)

sh.notes(322, 283, general_notes(STEP, extra=[
    "Material AISI 303 (1.4305), with certificate (the model shows 304).",
    "Passivate ASTM A967.",
    "Datums: E back face; F pin-hole pattern A1-A3; G Ø20 pilot axis.",
    "Ø20 g6 pilots the arm (or the lathe chuck backplate's Ø20 H7 bore).",
    "Model: STEVE part d93731cc revision 5.",
]), width=86, h=1.8, gap=1.0)
sh.title_block(fields(PART, "Planet carrier, front disk + output hub", "1", "AISI 303 (1.4305)",
                      "Passivate ASTM A967", "2:1", STEP, part_doc="STEVE part d93731cc rev 5"))
finish(sh, PART)
