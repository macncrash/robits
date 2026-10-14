"""Disc sander on a bench stand, driven by a second unknown-machine joint actuator (the accessory catalogue).

A separate machine, not a lathe attachment: a complete actuator (linked design, revision 36) on its bolted
pedestal, lifted on a riser block, turns a Ø250 (10 in) platen through a 303 hub on the output disk's six M4 load
holes. Geared 5:1, so up to 1060 rpm (13.9 m/s at the rim) with 10 N m continuous and 18 N m short-term at the
disc: slow for wood, right for metal (deburring, squaring, edge work) without burning the edge, and it does not
bog down when the work is pressed hard.

- Tilting table 0-45 degrees on two trunnions with a virtual pivot at the near edge, an engraved degree scale and
  lock knobs; 3/4 in miter slot and a miter gauge with a +-60 degree protractor.
- Steel guard round the rim and behind the disc, dust hood with a 2.5 in (Ø63) vacuum port.
- Welded open stand, table top at 875 mm.

Frame: disc axis along -Y (x 0, z 0), abrasive face toward the operator at -Y, Z up. The actuator, modelled with
its axis along +Z and its pedestal toward -Y, is turned 90 degrees about X (its axis -> -Y, its up -> Z).
"""
from steve import Design
from sander_params import table_y, table_z
from links import actuator
from components.riser import riser
from components.stand import stand
from components.sander_hub import sander_hub
from components.platen import platen
from components.abrasive import abrasive
from components.guard import guard
from components.trunnions import trunnions
from components.table import table
from components.miter_gauge import miter_gauge

TURN = ((0, 0, 0), ("X", 90))                         # actuator frame -> sander frame

design = Design("Disc sander (unknown-machine actuator) on bench stand")
design.add(actuator(), at=TURN, name="headstock")
for part in (riser, stand, sander_hub, platen, abrasive, guard, trunnions, table, miter_gauge):
    design.add(part)

# --- Motion ---
design.revolute("disc_spin", "headstock", "sander_hub", axis=((0, 0, 0), (0, -1, 0)))   # anticlockwise from the front
design.rigid("platen_screws", "sander_hub", "platen")
design.rigid("abrasive_stuck", "platen", "abrasive")
design.revolute("table_tilt", "trunnions", "table", axis=((0, table_y, table_z), (1, 0, 0)), limits=(0, 45))
design.slider("miter_slide", "table", "miter_gauge", axis="X", limits=(-50, 50))
design.rigid("riser_bolts", "stand", "riser")
design.rigid("guard_bolts", "stand", "guard")
design.rigid("trunnion_bolts", "stand", "trunnions")

design.pose("bevel_45", table_tilt=45)
design.animation("sanding", [({"disc_spin": 0, "table_tilt": 0, "miter_slide": 0}, 0),
                             ({"disc_spin": 3600, "miter_slide": -40}, 3),
                             ({"disc_spin": 7200, "table_tilt": 45, "miter_slide": -40}, 6),
                             ({"disc_spin": 10800, "table_tilt": 0, "miter_slide": 0}, 9)], loop=True)

# --- Designed contacts; everything else must not touch ---
for a, b in [("headstock", "riser"), ("riser", "stand"), ("sander_hub", "headstock"), ("platen", "sander_hub"),
             ("abrasive", "platen"), ("guard", "stand"), ("trunnions", "stand"), ("table", "trunnions"),
             ("miter_gauge", "table")]:
    design.contact(a, b, kind="seated")
design.fit_check("fit", motion=False, poses=["bevel_45"])

result = design.result()
