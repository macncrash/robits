"""AM-12 Readhead standoff, 4 off (spec: cnc/standoff.md)."""
import numpy as np

from common import *  # noqa: F403

PART = "AM-12-standoff"
STEP = "standoff.step"
s = load(STEP)
q = Q(s)
body = q.cyl(4.0)
stud = q.cyl(2.0)
tap = q.cyl(1.6)
for z in (-7.38, 0, 4):
    q.plane(z)
check(PART, "body length", 7.38, 0 - (-7.38))
check(PART, "stud length", stud["z1"] - stud["z0"], 4.0)
tap_depth = tap["z1"] - tap["z0"]
check(PART, "tapped hole drill depth vs 5 full thread (needs ~6 drilled)", tap_depth, 6.0, tol=0.01)
assert not [c for c in q.cyls if 1.65 < 2 * c["r"] < 1.99], "undercut found"
DISAGREEMENTS.append((PART, "stud undercut at the shoulder: sheet asks for one, model has none (plain Ø2 stud to "
                            "the shoulder); drawn as the model with a note allowing a thread undercut"))

sh = Sheet("A4")
vA = View((0, -1, 0), (0, 0, 1))
cut, loops = section(s, vA, (0, 0, 0))
k = 10.0
A = PView(sh, vA, (128 - k * (-1.69), 152), k, geo=project(cut, vA, hidden=False), loops=loops,
          label="SECTION A-A (10:1)", label_pos=(128, 191), ref=(128, 152))
P = lambda x, z: (x, 0, z)  # noqa: E731
A.centreline(P(0, -8), P(0, 4.6))
d4 = sh.dim(A, P(2, -3), P(-2, -3), "v", pos=-78, prefix="Ø", tol="±0.05", dec=1, part=PART, nominal=4)
sh.datum(d4[0], (0, -1), "A", L=3)
sh.dim(A, P(-2, -7.38), P(-2, 0), "h", pos=30, tol="-0.02/-0.05", dec=2, part=PART, nominal=7.38,
       label="body length (shoulder face to readhead face)")
sh.dim(A, P(-1, 0), P(-1, 4), "h", pos=30, dec=1, part=PART, nominal=4, label="stud")
sh.leader(A.P(P(-1, 2.5)), (205, 178), ["M2-6g stud (Loctite 243 into AM-02)", "thread undercut DIN 76 at the",
                                         "shoulder permitted (not modelled)"], h=1.9)
sh.leader(A.P(P(0.8, -4)), (205, 128), ["M2-6H, drill Ø1.6 × 5 (model);", "thread as deep as the drill allows,",
                                         "≥4.4 full (ISO 4762 M2×6 through", "the readhead PCB engages 4.4)"], h=1.9)
fp = sh.fcf(40, 110, "perpendicularity", "0.01", ["A"])
sh.fcf_leader(fp, A.P(P(1.4, -7.38)), from_side="right")
sh.text(fp[0], fp[1] - 3.4, "readhead face", h=1.8)
fq = sh.fcf(140, 112, "parallelism", "0.01", ["B"])
sh.fcf(fq[0], fq[1] - 5, "perpendicularity", "0.01", ["A"])
sh.fcf_leader(fq, A.P(P(1.6, 0)), from_side="left")
sh.datum(A.P(P(1.5, -7.38)) + (-0.1, 0), (-1, 0), "B", L=12)
sh.text(fq[2] + 1.5, fq[1] + 1.3, "shoulder face", h=1.8)
sh.leader(A.P(P(-1.85, -7.25)), (66, 176), "0.2×45° both body ends", h=1.9, side="left")

sh.notes(22, 86, general_notes(STEP, extra=[
    "Material AISI 303 (1.4305) (model shows 304). Passivate ASTM A967. Swiss or bar lathe.",
    "Make all four in one batch, length matched within 0.01; shim with RLS MB-ACC shims until the readhead LED "
    "is green (2.88 ±0.13 ring-to-readhead gap). Order spares.",
    "Alternative: bought M2 male-female Ø4 standoffs (303 or brass) faced to 7.36 ±0.01.",
], edges="-0.2"), width=84, h=1.7, gap=0.9)
tf = fields(PART, "Readhead standoff", "4", "AISI 303 (1.4305)", "Passivate ASTM A967", "10:1", STEP)
tf["edges"] = "-0.2 unless shown"
sh.title_block(tf)
finish(sh, PART)
