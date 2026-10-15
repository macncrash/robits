"""AM-05 Pedestal (spec: cnc/pedestal.md). STEVE part 0a76af67 rev 8."""
import numpy as np

from common import *  # noqa: F403
from amdraw import detail, cutting_line, triad, tag, view_arrow

PART = "AM-05-pedestal"
STEP = "pedestal.step"
s = load(STEP)
q = Q(s)

sad = q.cyl(120.0)
sad96 = q.cyl(96.0)
bolt = q.cyl(9.0, axis=(0, 1, 0), n=4)
cb = q.cyl(9.5, axis=(0, 1, 0), n=4)
thr = q.cyl(5.5, axis=(0, 1, 0), n=4)
dow = q.cyl(4.0, axis=(0, 1, 0), n=2)
port = q.cyl(8.0, axis=(1, 0, 0))
check(PART, "saddle Ø120 length", sad["z1"] - sad["z0"], 30.0)
check(PART, "counterbore depth from underside", -66 - (-88), 22.0)
q.plane(-88, normal=(0, 1, 0)); q.plane(-78, normal=(0, 1, 0)); q.plane(-30, normal=(0, 1, 0))
q.plane(-66, normal=(0, 1, 0))

sh = Sheet("A3")
# ---- SECTION A-A at z = 28 (through cbores C1, C2), seen from +Z
vA = View((0, 0, 1), (1, 0, 0))
cut, loops = section(s, vA, (0, 0, 28))
A = PView(sh, vA, (235, 266), 1.0, geo=project(cut, vA, hidden=False), loops=loops, label="SECTION A-A",
          label_pos=(235, 279), ref=(235, 209))
XY = lambda x, y: (x, y, 28)  # noqa: E731
sh.dim(A, XY(-65, -88), XY(65, -88), "h", pos=-44, part=PART, nominal=130)
sh.dim(A, XY(-40, -30), XY(40, -30), "h", pos=37, part=PART, nominal=80)
sh.dim(A, XY(-16, -88), XY(16, -88), "h", pos=-36, part=PART, nominal=32, label="screw rows x ±16")
sh.dim(A, XY(65, -88), XY(65, -78), "v", pos=70, part=PART, nominal=10, outside=True, tshift=-10)
sh.dim(A, XY(40, -88), XY(40, -30), "v", pos=78, part=PART, nominal=58)
u = np.array([0.5, 0.866])
sh.datum(A.P(XY(-30.0, -51.96)) + u * 0.1, u, "F", L=6)
d1 = sh.leader(A.P(XY(-22.0, -55.8)), (160, 276), ["Ø120 +0.03/0 (datum F)", "cylindricity 0.02, Ra 1.6"],
               h=2.0, side="left")
sh.leader(A.P(XY(-16, -80)), (222, 150), ["4× Ø5.5 THRU, cbore Ø9.5 × 22 deep", "from underside (to Y -66),",
                                          "position Ø0.2 to the dowels"], h=1.9, side="left")
sh.dim(A, XY(-16, -88), XY(-16, -66), "v", pos=-75, part=PART, nominal=22, label="cbore depth")
sh.dim(A, XY(0, 0), XY(-65, -88), "v", pos=-66, part=PART, nominal=88, label="axis height", tshift=-24)
A.centreline(XY(-16, -90), XY(-16, -50), ext=1); A.centreline(XY(16, -90), XY(16, -50), ext=1)
A.centreline(XY(0, -92), XY(0, -26), ext=1)
fsx = sh.fcf(138, 177, "flatness", "0.05")
sh.fcf_leader(fsx, A.P(XY(-62, -88)), from_side="right")
sh.text(fsx[0], fsx[1] - 3.5, "base underside", h=1.8)

# ---- SECTION B-B at x = 0 (dowels, cable slot, saddle step), seen from +X: placed left (first angle)
vB = View((1, 0, 0), (0, 0, -1))
cutB, loopsB = section(s, vB, (0, 0, 0))
B = PView(sh, vB, (100, 262), 1.0, geo=project(cutB, vB, hidden=False), loops=loopsB, label="SECTION B-B",
          label_pos=(80, 279), ref=(80, 209))
cutting_line(sh, A, (0, -24, 28), (0, -94, 28), "B", look=(-1, 0))
YZ = lambda y, z: (0, y, z)  # noqa: E731
sh.dim(B, YZ(-88, -28), YZ(-88, 72), "h", pos=-58, part=PART, nominal=100)
sh.dim(B, YZ(-30, -20), YZ(-30, 44), "h", pos=37, part=PART, nominal=64)
sh.dim(B, YZ(-60, 14), YZ(-60, 44), "h", pos=28, part=PART, nominal=30, label="Ø120 saddle length")
for z in (22, 40):
    B.centreline(YZ(-67, z), YZ(-56, z), ext=1)
sh.dim(B, YZ(-88, 22), YZ(-88, 40), "h", pos=-42, tol="±0.01", dec=2, part=PART, nominal=18, label="dowel pitch")
sh.dim(B, YZ(-88, 40), YZ(-78, 44), "h", pos=-50, part=PART, nominal=4, outside=True, tshift=-7)
sh.leader(B.P(YZ(-62, 22)), (28, 139), ["2× Ø4 N7 (-0.004/-0.016), 6 deep", "from the saddle (drill 7 + 118°)",
                                         "position Ø0.02 to F and each other", "(±0.01); ISO 8734 4 m6 pressed"],
          h=1.9, side="right")
sh.dim(B, YZ(-88, 6), YZ(-88, 20), "h", pos=-50, part=PART, nominal=14, tol="±0.2", dec=1, label="slot length")
sh.dim(B, YZ(-78, -28), YZ(-78, -20), "h", pos=-42, part=PART, nominal=8, outside=True, tshift=-9)
sh.leader(B.P(YZ(-70, 16)), (136, 196), ["cable slot 8 ±0.2 wide (Y -74..-66),", "R4 ends, through in X",
                                          "(Ø8 end mill from both sides)"], h=1.8, side="right")
sh.leader(B.P(YZ(-48, 14)), (125, 254), ["Ø96 +0.03/0, coaxial with F within Ø0.02",
                                         "step: 0.5×45° on its inner edge"], h=1.9, side="left")
sh.dim(B, YZ(-48, -20), YZ(-48, 14), "h", pos=28, part=PART, nominal=34, label="Ø96 saddle length")

# ---- VIEW C from above (+Y), holes
vC = View((0, 1, 0), (1, 0, 0))
C = PView(sh, vC, (115, 92), 1.0, geo=project(s, vC, hidden=False), label="VIEW C (from above)",
          label_pos=(70, 124), ref=(115, 72))
view_arrow(sh, A.P(XY(52, -20)), (0, -1), "C")
XZ = lambda x, z: (x, -78, z)  # noqa: E731
sh.dim(C, XZ(-52, -15), XZ(52, -15), "h", pos=-52, part=PART, nominal=104)
sh.dim(C, XZ(52, -15), XZ(52, 59), "v", pos=74, part=PART, nominal=74)
sh.dim(C, XZ(65, 72), XZ(52, 59), "h", pos=-52, part=PART, nominal=13, outside=True, tshift=9)
sh.dim(C, XZ(16, 28), XZ(16, 37), "v", pos=-75, part=PART, nominal=9, label="screw rows z 28 / 37", outside=True,
       tshift=9)
sh.dim(C, XZ(16, 37), XZ(65, 72), "v", pos=-75, part=PART, nominal=35, label="z 37 to base end", ext_b=True)
sh.leader(C.P(XZ(52, -15)) + (3.2, 3.2), (192, 118), ["4× Ø9 ±0.1 THRU", "position Ø0.3 (M8)"], h=1.9,
          side="right")
sh.leader(C.P(XZ(65, 64)), (195, 26), "R10 (4 corners)", h=1.9)
for x in (-52, 52):
    for z in (-15, 59):
        C.centremark(XZ(x, z), 4.5, ext=1.5)

sh.notes(322, 245, general_notes(STEP, extra=[
    "Material EN AW-6061-T6 (T6511 plate or rectangle bar), with certificate.",
    "Black anodise MIL-A-8625 Type II. MASK the saddle bores (chromate conversion there: thermal joint) and the "
    "dowel holes.",
    "Datum F: Ø120 saddle axis (= housing axis). Saddle bores by circular interpolation or a boring head with "
    "the part on end; Ø120 and Ø96 in one setup if possible.",
    "Saddle +0.00/+0.03 suits thermal paste. A 0.23-0.25 mm pad needs about Ø120.5: decide pad or paste before "
    "machining (open question).",
    "Ø5.5 holes break out through the curved saddle with a feather edge: deburr.",
    "Dowel holes are blind: leave an air vent or press slowly.",
    "Model frame: STEVE part 0a76af67 revision 8 = actuator frame (axis Z, pedestal toward -Y).",
]), width=86, h=1.8, gap=1.0)
sh.title_block(fields(PART, "Pedestal", "1", "EN AW-6061-T6", "Black anodise Type II, saddle chromate",
                      "1:1", STEP, part_doc="STEVE part 0a76af67 rev 8"))
finish(sh, PART)
