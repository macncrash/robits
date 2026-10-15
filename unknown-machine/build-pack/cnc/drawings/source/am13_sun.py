"""AM-13 Sun gear m1 18 T (spec: cnc/sun.md, hardware/gears.md)."""
import numpy as np

from common import *  # noqa: F403
from amdraw import cutting_line, triad
from gearsheet import gear_views, gear_notes

PART = "AM-13-sun"
STEP = "sun.step"
s = load(STEP)
q = Q(s)
from geom import radial_extent
r_tip = radial_extent(s)[1]
check(PART, "tip diameter", 2 * r_tip, 20.0, tol=0.01)
rnd = q.cyl(12.0)
fl = q.plane(5.4, normal=(1, 0, 0)), q.plane(-5.4, normal=(1, 0, 0))
for z in (48, 60):
    q.plane(z)
check(PART, "face width", 60 - 48, 12.0)
check(PART, "bore across flats", fl[0] - fl[1], 10.8)
# root circle from the model's root fillets (R0.38 centred on r = 7.75 + 0.38)
root_r = min(np.hypot(*c[:2]) for c in Q(s).cyl(0.76, n=None)["centres"]) - 0.38
check(PART, "root diameter", 2 * root_r, 15.5, tol=0.01)

sh = Sheet("A3")
F, A = gear_views(sh, s, 48, 60, 5.0, (82, 190), 200, 258)
F.pcd(9.0, centre=(0, 0, 60))
F.centreline((-12, 0, 60), (12, 0, 60), ext=0); F.centreline((0, -12, 60), (0, 12, 60), ext=0)
triad(sh, F, (30, 262))
cutting_line(sh, F, (0, 11.5, 60), (0, -11.5, 60), "A", look=(1, 0))
sh.dim(F, (-5.4, 0, 60), (5.4, 0, 60), "h", pos=-72, tol="+0.02/0", dec=2, part=PART, nominal=10.8,
       label="double-D across flats")
fsym = sh.fcf(42, 100, "symmetry", "0.02", ["A"])
sh.text(fsym[2] + 1.5, fsym[1] + 1.3, "flats to A", h=1.8)
sh.leader(F.P((-4.24, -4.24, 60)), (30, 134), ["Ø12 H7 (+0.018/0) round portions,",
                                               "wire-EDM after hardening"], h=1.9, side="right")
sh.text(F.c[0] + 9.5 * 5 * 0.71 + 3, F.c[1] + 9 * 5 * 0.71 + 2, "pitch Ø18", h=1.8, check=False)

P = lambda y, z: (0, y, z)  # noqa: E731   section plane x = 0, paper up = +Y
A.centreline(P(0, 46), P(0, 62))
for xx in (-9, 9):
    A.centreline(P(xx, 47), P(xx, 61), ext=2)     # pitch line (ISO 2203)
dA = sh.dim(A, P(6, 54), P(-6, 54), "v", pos=-45, prefix="Ø", tol="H7 (+0.018/0)", part=PART, nominal=12,
            outside=True, tshift=-24)
sh.datum(dA[1], (0, 1), "A", L=3)
sh.dim(A, P(10, 50), P(-10, 50), "v", pos=48, prefix="Ø", tol="h11 (0/-0.13)", dec=2, part=PART, nominal=20)
sh.dim(A, P(-7.75, 49), P(7.75, 49), "v", pos=58, text="(Ø15.50)", label="root (reference)")
sh.dim(A, P(-10, 48), P(-10, 60), "h", pos=-64, tol="-0.05/-0.10", dec=2, part=PART, nominal=12, label="face width")
sh.datum(A.P(P(7.6, 48)) + (-0.1, 0), (-1, 0), "B", L=6)
fp = sh.fcf(232, 132, "parallelism", "0.01", ["B"])
sh.fcf(fp[0], fp[1] - 5, "perpendicularity", "0.01", ["A"])
sh.fcf_leader(fp, A.P(P(8, 60)), from_side="left")
sh.text(fp[0], fp[1] - 8.6, "front face", h=1.8)
sh.leader(A.P(P(6.2, 59.8)), (240, 155), "0.5×45° bore lead-in, both ends", h=1.9)
sh.leader(A.P(P(10, 59.85)), (205, 276), "tip chamfer 0.2×45° both ends", h=1.9, side="left")

rows = [["GEAR DATA", ""],
        ["Module m (normal)", "1"], ["Number of teeth z", "18"], ["Pressure angle α", "20°"],
        ["Helix angle β", "0° (spur)"], ["Profile shift coefficient x", "0"],
        ["Basic rack", "ISO 53 profile A (ha* 1.0, hf* 1.25, ρf* 0.38)"],
        ["Reference (pitch) diameter d", "18.000"], ["Tip diameter da", "20.00 h11 (0/-0.13)"],
        ["Root diameter df", "15.50 (generated)"], ["Face width b", "12.00 -0.05/-0.10"],
        ["Span over k = 3 teeth W3", "7.632 nom.; make 7.607 / 7.587 (-0.025/-0.045)"],
        ["Over 2 pins Ø1.75 Md (alt.)", "20.458 nom.; allowance ≈1.5×: -0.038/-0.068 (ref.)"],
        ["Working backlash", "0.03-0.08 at a = 22.500 (tooth thinning above)"],
        ["Accuracy", "ISO 1328-1:2013 grade 6, teeth ground after HT"],
        ["Runout of teeth (pitch circle) to A", "0.01"],
        ["Mating gears", "3 × planet AM-14 (z 27), a = 22.500"],
        ["Material", "18CrNiMo7-6 (1.6587); AISI 9310 / 8620 with cert."],
        ["Heat treatment", "carburise, quench, temper"],
        ["Surface hardness", "58-62 HRC"], ["Case depth", "Eht 0.3-0.5 mm to 550 HV1, after grinding"],
        ["Core hardness", "30-42 HRC"], ["Tooth ends", "tip chamfer 0.2×45°"]]
sh.table(262, 283, [52, 96], rows, h=1.9, row_h=3.75, bold_first_col=False)

sh.notes(22, 92, general_notes(STEP, threads=False, extra=gear_notes([
    "Bore: double-D, Ø12 H7 round portions, 10.80 +0.02/0 across the flats, wire-EDM after hardening (fits the "
    "shaft AM-09 flats 10.80 -0.01/-0.03; slides off forward).",
    "Thin rim (1.75 mm under the root): control heat-treat distortion; check the rim is not through-hardened.",
    "Inspection: gear report per ISO 1328 (profile, helix, pitch, runout), W3, hardness and case depth on a "
    "coupon from the same batch. Supply material certificate.",
])), width=200, h=1.8, gap=0.95)
sh.title_block(fields(PART, "Sun gear m1 18 T", "1", "18CrNiMo7-6 (1.6587)",
                      "Carburised 58-62 HRC, Eht 0.3-0.5, ground", "5:1", STEP))
finish(sh, PART)
