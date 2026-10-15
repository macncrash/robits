"""AM-14 Planet gear m1 27 T, 3 per actuator (spec: cnc/planet.md, hardware/gears.md)."""
import numpy as np

from common import *  # noqa: F403
from amdraw import cutting_line, triad
from gearsheet import gear_views, gear_notes
from geom import radial_extent

PART = "AM-14-planet"
STEP = "planet.step"
s = load(STEP)
q = Q(s)
bore = q.cyl(10.0)
r_tip = radial_extent(s)[1]
check(PART, "tip diameter", 2 * r_tip, 29.0, tol=0.01)
root_r = min(np.hypot(*c[:2]) for c in q.cyl(0.76)["centres"]) - 0.38
check(PART, "root diameter", 2 * root_r, 24.5, tol=0.01)
for z in (0, 12):
    q.plane(z)

sh = Sheet("A3")
F, A = gear_views(sh, s, 0, 12, 5.0, (101, 192), 215, 272, plane="y")
F.pcd(13.5, centre=(0, 0, 12))
F.centreline((-16, 0, 12), (16, 0, 12), ext=0); F.centreline((0, -16, 12), (0, 16, 12), ext=0)
triad(sh, F, (28, 276))
cutting_line(sh, F, (-14.9, 0, 12), (14.9, 0, 12), "A", look=(0, 1))
sh.text(F.c[0] + 13.5 * 5 * 0.72 + 4, F.c[1] + 13.5 * 5 * 0.72 + 3, "pitch Ø27", h=1.8, check=False)

P = lambda x, z: (x, 0, z)  # noqa: E731   section plane y = 0, paper up = -X
A.centreline(P(0, -2), P(0, 14))
for xx in (-13.5, 13.5):
    A.centreline(P(xx, -1), P(xx, 13), ext=2)
dA = sh.dim(A, P(5, 6), P(-5, 6), "v", pos=-36, prefix="Ø", tol="N6 (-0.007/-0.016)", part=PART, nominal=10,
            outside=True, tshift=-33)
sh.datum(dA[1] + (0, 7), (0, 1), "A", L=3)
sh.rough_leader(A.P(P(5, 3)), (A.ref[0] + 70, A.ref[1] - 56), "Ra 0.8")
sh.dim(A, P(14.5, 4), P(-14.5, 4), "v", pos=42, prefix="Ø", tol="h11 (0/-0.13)", dec=2, part=PART, nominal=29)
sh.dim(A, P(-12.25, 9), P(12.25, 9), "v", pos=52, text="(Ø24.50)", label="root (reference)")
sh.dim(A, P(14.5, 0), P(14.5, 12), "h", pos=-82, tol="-0.05/-0.10", dec=2, part=PART, nominal=12, label="face width")
sh.datum(A.P(P(-9, 0)) + (-0.1, 0), (-1, 0), "B", L=6)
fp = sh.fcf(A.ref[0] + 66, A.ref[1] - 20, "parallelism", "0.01", ["B"])
sh.fcf_leader(fp, A.P(P(9, 12)), from_side="left")
sh.text(fp[0], fp[1] - 3.4, "front face", h=1.8)
sh.leader(A.P(P(5.15, 11.85)), (A.ref[0] + 66, A.ref[1] - 36), "0.3×45° bore lead-in, both ends", h=1.9)
sh.leader(A.P(P(14.5, 11.85)), (A.ref[0] + 66, A.ref[1] - 80), "tip chamfer 0.2×45° both ends", h=1.9)

rows = [["GEAR DATA", ""],
        ["Module m (normal)", "1"], ["Number of teeth z", "27"], ["Pressure angle α", "20°"],
        ["Helix angle β", "0° (spur)"], ["Profile shift coefficient x", "0"],
        ["Basic rack", "ISO 53 profile A (ha* 1.0, hf* 1.25, ρf* 0.38)"],
        ["Reference (pitch) diameter d", "27.000"], ["Tip diameter da", "29.00 h11 (0/-0.13)"],
        ["Root diameter df", "24.50 (generated)"], ["Face width b", "12.00 -0.05/-0.10"],
        ["Span over k = 4 teeth W4", "10.711 nom.; make 10.686 / 10.666 (-0.025/-0.045)"],
        ["Over 2 pins Ø1.75 Md (alt.)", "29.435 nom. (odd z: pins in opposite gaps)"],
        ["Working backlash", "0.03-0.08 with the sun at a = 22.500"],
        ["Accuracy", "ISO 1328-1:2013 grade 6, teeth ground after HT"],
        ["Runout of teeth (pitch circle) to A", "0.01"],
        ["Mating gears", "sun AM-13 (z 18, a = 22.5), ring AM-15 (z 72 int.)"],
        ["Material", "18CrNiMo7-6 (1.6587); AISI 9310 / 8620 with cert."],
        ["Heat treatment", "carburise, quench, temper"],
        ["Surface hardness", "58-62 HRC"], ["Case depth", "Eht 0.3-0.5 mm to 550 HV1, after grinding"],
        ["Core hardness", "30-42 HRC"], ["Tooth ends", "tip chamfer 0.2×45°"]]
sh.table(22, 101, [52, 96], rows, h=1.9, row_h=3.75)

sh.notes(270, 283, general_notes(STEP, threads=False, extra=gear_notes([
    "Bore Ø10 N6 for the INA HK0609 drawn cup (pressed in): grind after hardening, Ra 0.8, runout of the "
    "pitch circle to the bore (A) 0.01. Faces parallel 0.01.",
    "Quantity 3 per actuator; order 4 (one spare).",
    "Inspection: gear report per ISO 1328, W4, hardness and case depth on a coupon from the same batch. Supply "
    "material certificate.",
])), width=140, h=1.8, gap=0.95)
sh.title_block(fields(PART, "Planet gear m1 27 T", "3 (+1 spare)", "18CrNiMo7-6 (1.6587)",
                      "Carburised 58-62 HRC, Eht 0.3-0.5, ground", "5:1", STEP))
finish(sh, PART)
