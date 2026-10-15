"""AM-06 Planet carrier, rear part (spec: cnc/carrier.md). STEVE part 06b08578 rev 8."""
import numpy as np

from common import *  # noqa: F403
from amdraw import detail, cutting_line, triad, tag

PART = "AM-06-carrier"
STEP = "carrier.step"
s = load(STEP)
q = Q(s)

sleeve = q.cyl(35.0)
shoulder = q.cyl(41.0)
plate = q.cyl(66.0)
seat = q.cyl(16.0)
clr = q.cyl(14.0)
groove = q.cyl(33.0)
posts = q.cyl(12.0, n=3)
pins = q.cyl(6.0, n=3)
m4 = q.cyl(3.3, n=3)
for z in (27.9, 30.9, 32.5, 37, 42.5, 44.5, 47.5, 60.5):
    q.plane(z)
check(PART, "groove width", groove["z1"] - groove["z0"], 1.6)
check(PART, "groove front wall to shoulder face", 42.5 - groove["z1"], 10.0)
check(PART, "M4 tap drill depth", 60.5 - m4["z0"], 13.0)
for c in pins["centres"]:
    check(PART, "pin pitch radius", float(np.hypot(c[0], c[1])), 22.5, tol=0.0005)

sh = Sheet("A3")
# ---- front view (+Z), 2:1
vF = View((0, 0, 1), (1, 0, 0))
F = PView(sh, vF, (96, 206), 2.0, geo=project(s, vF, hidden=False), label="VIEW FROM FRONT (2:1)",
          label_pos=(96, 276))
F.pcd(22.5, centre=(0, 0, 60.5))
F.centreline((-36, 0, 60.5), (36, 0, 60.5), ext=0); F.centreline((0, -36, 60.5), (0, 36, 60.5), ext=0)
triad(sh, F, (30, 270))
cutting_line(sh, F, (-34.5, 0, 60.5), (34.5, 0, 60.5), "A", look=(0, 1))
ang = lambda c: np.arctan2(c[1], c[0]) % (2 * np.pi)  # noqa: E731
rows = [["TAG", "X", "Y", "HOLE", "DEPTH / NOTE"]]
for i, c in enumerate(sorted(pins["centres"], key=ang)):
    a = ang(c)
    tag(sh, F, (c[0], c[1], 60.5), f"A{i + 1}", off=(9 * np.cos(a) - 2, 9 * np.sin(a) + 3))
    rows.append([f"A{i + 1}", fmt(c[0], 3), fmt(c[1], 3), "Ø6 N7 (-0.004/-0.016)", "THRU plate (3)"])
for i, c in enumerate(sorted(m4["centres"], key=ang)):
    a = ang(c)
    tag(sh, F, (c[0], c[1], 60.5), f"B{i + 1}", off=(16 * np.cos(a), 16 * np.sin(a)))
    rows.append([f"B{i + 1}", fmt(c[0], 3), fmt(c[1], 3), "M4-6H, drill Ø3.3", "11.5 thd / 13 drill"])
x1, y1 = sh.table(24, 128, [9, 17, 17, 38, 33], rows, h=1.9, row_h=3.7)
sh.notes(24, y1 - 4, [
    "X/Y in the STEP frame (Z axis = datum D), from post front faces (Z 60.5).",
    "A1-A3: co-drill Ø5.8 with AM-07 clamped on (pins and screws in place), then ream Ø6 N7 here. "
    "True position Ø0.01 to D; pitch circle R22.500 ±0.005 (sets the gear centre distance). "
    "ISO 8734 6 m6 × 18 hardened pins pressed in.",
    "B1-B3 (posts): position Ø0.1 to D. ISO 10642 M4×16 from AM-07, 11 engaged.",
], title=None, width=124, h=1.9, gap=1.05)

# ---- SECTION A-A (plane y = 0, seen from -Y... arrows point +Y), 2:1: paper right = +Z, up = -X
vA = View((0, -1, 0), (0, 0, 1))
cut, loops = section(s, vA, (0, 0, 0))
k = 2.0
RX, RY = 222, 192
A = PView(sh, vA, (RX - 2 * 44.2, RY), k, geo=project(cut, vA, hidden=False), loops=loops,
          label="SECTION A-A (2:1)", label_pos=(RX, 276), ref=(RX, RY))
P = lambda x, z: (x, 0, z)  # noqa: E731
A.centreline(P(0, 26), P(0, 62))
A.centreline(P(-22.5, 46), P(-22.5, 62), ext=1); A.centreline(P(22.5, 43.5), P(22.5, 48.5), ext=1)
d35 = sh.dim(A, P(17.5, 34), P(-17.5, 34), "v", pos=-40, prefix="Ø", tol="h5 (0/-0.011)", part=PART, nominal=35)
sh.datum(d35[0], (0, -1), "D", L=3)
fcy = sh.fcf(d35[0][0] - 2, d35[0][1] - 26, "cylindricity", "0.004", anchor="right")
sh.fcf_leader(fcy, (d35[0][0], d35[0][1] - 16), from_side="right")
sh.rough_leader(A.P(P(17.5, 30)), (RX - 52, 140), "Ra 0.4")
sh.dim(A, P(20.5, 43.5), P(-20.5, 43.5), "v", pos=-48, prefix="Ø", part=PART, nominal=41, tshift=-30)
sh.dim(A, P(7, 30), P(-7, 30), "v", pos=-56, prefix="Ø", tol="±0.1", part=PART, nominal=14)
d16 = sh.dim(A, P(8, 46), P(-8, 46), "v", pos=40, prefix="Ø", tol="N6 (-0.009/-0.020)", part=PART, nominal=16,
             outside=True, tshift=26)
fco = sh.fcf(d16[1][0] + 2, d16[1][1] + 30, "coaxiality", "0.01", ["D"], dia=True)
sh.fcf_leader(fco, (d16[1][0], d16[1][1] + 8), from_side="left")
sh.dim(A, P(33, 47.5), P(-33, 47.5), "v", pos=50, prefix="Ø", part=PART, nominal=66)
# axial
sh.dim(A, P(17.5, 27.9), P(-28.5, 60.5), "h", pos=-80, part=PART, nominal=32.6, label="overall length")
sh.dim(A, P(17.5, 27.9), P(20.5, 42.5), "h", pos=-72, part=PART, nominal=14.6, label="sleeve to shoulder face")
sh.dim(A, P(20.5, 42.5), P(33, 44.5), "h", pos=-72, part=PART, nominal=2, outside=True, tshift=0)
sh.dim(A, P(33, 44.5), P(33, 47.5), "h", pos=-72, part=PART, nominal=3, outside=True, tshift=8)
sh.dim(A, P(-28.5, 47.5), P(-28.5, 60.5), "h", pos=72, part=PART, nominal=13, label="posts")
sh.dim(A, P(-8, 37), P(-8, 47.5), "h", pos=62, part=PART, nominal=10.5, label="HK1210 seat depth")
fpo = sh.fcf(RX + 30, 276 - 13, "flatness", "0.01")
sh.fcf(fpo[0], fpo[1] - 5, "perpendicularity", "0.01", ["D"])
sh.fcf_leader(fpo, A.P(P(-25, 60.5)), from_side="left")
sh.text(fpo[2] + 1.5, fpo[1] + 1.3, "post front faces (common zone, all 3)", h=1.8)
fpl = sh.fcf(RX + 52, RY - 52, "perpendicularity", "0.02", ["D"])
sh.fcf_leader(fpl, A.P(P(28, 47.5)), from_side="left")
sh.text(fpl[0], fpl[1] - 3.4, "plate front face", h=1.8)
sh.leader(A.P(P(-22.5 + 1.65, 50)), (RX + 50, RY + 34), ["M4-6H (B1-B3): 11.5 full thread,", "drill Ø3.3 × 13, 118°"],
          h=1.9)
sh.leader(A.P(P(22.5 + 3, 46)), (RX + 50, RY - 34), ["Ø6 N7 (A1-A3), see table"], h=1.9)
sh.leader(A.P(P(-28.5, 48.2)), (RX + 50, RY + 54), ["post-root fillet R1 (bull-nose)", "posts Ø12 at R22.5"], h=1.9)

# ---- DETAIL B (5:1): DIN 471 groove, shoulder relief, shoulder fillet
B = detail(sh, A, P(-18.5, 37.5), 7.0, 4, (196, 46), "B", label_dy=2)
sh.dim(B, P(-16.5, 30.9), P(-16.5, 32.5), "h", pos=8, tol="+0.14/0", dec=2, part=PART, nominal=1.6,
       outside=True, tshift=-14, label="groove width")
sh.dim(B, P(-17.5, 32.5), P(-20.5, 42.5), "h", pos=17, tol="+0.05/0", dec=2, part=PART, nominal=10.0,
       label="groove front wall to shoulder face")
sh.leader(B.P(P(-16.5, 31.7)), (229, 104), ["DIN 471 35 groove", "Ø33.0 h12 (0/-0.25)"], h=1.9, side="right")
sh.leader(B.P(P(-17.8, 42.0)), (229, 95.5), "relief 0.3 × 0.3", h=1.9, side="right")
sh.leader(B.P(P(-20.6, 44.4)), (229, 88.5), "R0.4 shoulder-to-plate", h=1.9, side="right")
fsh = sh.fcf(229, 78, "perpendicularity", "0.005", ["D"])
sh.fcf_leader(fsh, B.P(P(-19.5, 42.5)), from_side="left")
sh.text(fsh[2] + 1.5, fsh[1] + 1.3, "shoulder face", h=1.8)

sh.notes(322, 283, general_notes(STEP, extra=[
    "Material AISI 303 (1.4305), annealed, cold finished, with certificate (the model shows 304).",
    "Passivate ASTM A967 (citric or nitric).",
    "Datum D: Ø35 h5 sleeve axis (CRBH 3510 inner-ring seat). 0.5×45° lead-ins at the sleeve rear end and the "
    "Ø16 seat entry.",
    "Ø16 N6 seat Ra 0.8 (INA HK1210 drawn cup).",
    "Inspect: CMM sleeve, seat coaxiality, shoulder perpendicularity, pin-hole positions (with AM-07).",
    "Model: STEVE part 06b08578 revision 8.",
]), width=86, h=1.8, gap=1.0)
sh.title_block(fields(PART, "Planet carrier, rear part", "1", "AISI 303 (1.4305)", "Passivate ASTM A967",
                      "2:1 (views as noted)", STEP, part_doc="STEVE part 06b08578 rev 8"))
finish(sh, PART)
