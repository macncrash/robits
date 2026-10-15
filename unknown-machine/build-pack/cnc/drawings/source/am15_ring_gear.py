"""AM-15 Ring gear m1 72 T internal (spec: cnc/ring_gear.md, hardware/gears.md)."""
import numpy as np

from common import *  # noqa: F403
from amdraw import cutting_line, triad
from gearsheet import gear_views, gear_notes
from geom import radial_extent

PART = "AM-15-ring_gear"
STEP = "ring_gear.step"
s = load(STEP)
q = Q(s)
od = q.cyl(86.0)
r_tip = radial_extent(s)[0]
check(PART, "tip (inside) diameter", 2 * r_tip, 70.0, tol=0.01)
root_r = max(np.hypot(*c[:2]) for c in q.cyl(0.76)["centres"]) + 0.38
check(PART, "root diameter", 2 * root_r, 74.5, tol=0.01)
for z in (48, 60):
    q.plane(z)

sh = Sheet("A3")
F, A = gear_views(sh, s, 48, 60, 2.0, (113, 182), 236, 275, plane="y", beyond=False)
for xx in (-35, 35):   # tip line of the teeth beyond the cutting plane (ISO 2203), with the 0.2 tip chamfers
    sh.line([A.P((xx, 0, 48.2)), A.P((xx, 0, 59.8))], w=0.5)
    for zz, dz in ((48.2, -0.2), (59.8, 0.2)):
        sh.line([A.P((xx, 0, zz)), A.P((xx + np.sign(xx) * 0.2, 0, zz + dz))], w=0.5)
F.pcd(36.0, centre=(0, 0, 60))
F.centreline((-45, 0, 60), (45, 0, 60), ext=0); F.centreline((0, -45, 60), (0, 45, 60), ext=0)
triad(sh, F, (30, 276))
cutting_line(sh, F, (-43.5, 0, 60), (43.5, 0, 60), "A", look=(0, 1), ext=2.5)
sh.leader(F.P((25.46, 25.46, 60)), (176, 262), "pitch Ø72", h=1.9)

P = lambda x, z: (x, 0, z)  # noqa: E731   section plane y = 0, paper up = -X
A.centreline(P(0, 46), P(0, 62))
for xx in (-36, 36):
    A.centreline(P(xx, 47), P(xx, 61), ext=2)
dA = sh.dim(A, P(43, 54), P(-43, 54), "v", pos=24, prefix="Ø", tol="s6 (+0.093/+0.071)", part=PART, nominal=86)
sh.datum(dA[1], (0, 1), "A", L=3)
sh.dim(A, P(35, 56), P(-35, 56), "v", pos=-26, prefix="Ø", tol="H11 (+0.19/0)", dec=2, part=PART, nominal=70,
       tshift=-34)
sh.dim(A, P(-37.25, 50), P(37.25, 50), "v", pos=-17, text="(Ø74.50)", label="root (reference)", tshift=40)
sh.dim(A, P(43, 48), P(43, 60), "h", pos=-100, tol="-0.05/-0.10", dec=2, part=PART, nominal=12, label="face width")
sh.datum(A.P(P(-40, 48)) + (-0.1, 0), (-1, 0), "B", L=6)
fp = sh.fcf(252, 120, "parallelism", "0.01", ["B"])
sh.fcf(fp[0], fp[1] - 5, "perpendicularity", "0.01", ["A"])
sh.fcf_leader(fp, A.P(P(40, 60)), from_side="left")
sh.text(fp[0], fp[1] - 8.6, "front face", h=1.8)
sh.rough_leader(A.P(P(43, 52)), (252, 102), "Ra 0.8")

rows = [["GEAR DATA", ""],
        ["Module m (normal)", "1"], ["Number of teeth z", "72 (internal)"], ["Pressure angle α", "20°"],
        ["Helix angle β", "0° (spur)"], ["Profile shift coefficient x", "0"],
        ["Basic rack", "ISO 53 profile A (root radius 0.38)"],
        ["Reference (pitch) diameter d", "72.000"], ["Tip diameter da (inside)", "70.00 H11 (+0.19/0)"],
        ["Root diameter df", "74.50 (generated)"], ["Face width b", "12.00 -0.05/-0.10"],
        ["Between 2 pins Ø1.68 Mi", "69.703 nom.; make 69.733 / 69.763 (+0.03/+0.06)"],
        ["", "(even z: opposite gaps; space widening for backlash)"],
        ["Accuracy", "ISO 1328-1:2013 grade 7 (shaped)"],
        ["Runout of teeth (pitch circle) to A", "0.015"],
        ["Mating gears", "3 × planet AM-14 (z 27)"],
        ["Material", "34CrNiMo6 +QT (1.6582); AISI 4340 with cert."],
        ["Heat treatment", "quench and temper before cutting"],
        ["Hardness", "28-34 HRC (about 280-320 HB)"],
        ["Optional", "gas nitriding after cutting: ≥550 HV, Nht 0.2-0.3"],
        ["Tooth ends", "tip chamfer 0.2×45°"]]
sh.table(262, 283, [52, 96], rows, h=1.9, row_h=3.75)

sh.notes(22, 86, general_notes(STEP, threads=False, extra=gear_notes([
    "Teeth shaped (Fellows) or, for one or two prototypes, wire-EDM cut. No catalogue m1 72 T internal gear exists.",
    "OD Ø86 s6 is pressed into the front flange AM-04 (Ø86 H7) with Loctite 638: 0.036-0.093 interference. The "
    "press fit squeezes the teeth inward by about 0.02 mm on the diameter: size Mi for it or check Mi after pressing.",
    "OD: 0.5×45° press lead-in chamfer at both ends. Tooth tips: 0.2×45° chamfer at both ends.",
    "Inspection: gear report per ISO 1328, Mi, hardness. Supply material certificate.",
])), width=200, h=1.8, gap=0.95)
sh.title_block(fields(PART, "Ring gear m1 72 T internal", "1", "34CrNiMo6 +QT (1.6582)",
                      "QT 28-34 HRC; gas nitriding optional", "2:1", STEP))
finish(sh, PART)
