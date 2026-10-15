"""Teardown order (service sequence), the flange screw pattern and the rear screw / encoder hole patterns."""
import math

SCREW_PCD = 100  # mm Flange screw pitch circle
SCREW_ANGLES = (45, 135, 225, 315)  # degrees


def _circle(r, angles):
    return [(round(r * math.cos(math.radians(a)), 4), round(r * math.sin(math.radians(a)), 4)) for a in angles]


BELL_SCREWS = _circle(46, (45, 135, 225, 315))       # end bell to housing, M4, PCD 92
CAP_SCREWS = _circle(37, (30, 150, 270))             # rear cap to end bell, M3
READHEAD_HOLES = _circle(24.5, (0, 60, 120, 180))    # AksIM-2 MB039 readhead holes / standoffs, R24.5
RING_SCREWS = _circle(12.5, [22.5 + 45 * k for k in range(8)])   # MRA039 ring screws, PCD 25

# Order checked with the animation's collision sweep. The ring gear is pressed into the flange (they come off
# together, then it is pressed out forward); flange and ring go well clear, because the carrier comes out next with
# the bearing clamp ring (captive under its plate) and the crossed-roller bearing (held on its sleeve). At the back
# the cap, then the encoder readhead, then the encoder hub with its ring come off before the end bell. The sun and
# the encoder hub ride on the rotor, so their slides back off while the rotor is pulled (their positions stay put).
STAGES = [
    ("flange screws out", {f"screw_{k}_out": 200 for k in range(1, 5)}),
    ("front flange + ring gear off", {"flange_out": 170, "ring_out": 170}),
    ("ring gear pressed out of the flange", {"ring_out": 195}),
    ("rear cap screws out", {f"cap_screw_{k}_out": -35 for k in range(1, 4)}),
    ("encoder cap off", {"cap_out": -270}),
    ("encoder readhead off (its screws with it)", {"readhead_out": -250}),
    ("encoder hub + ring off the shaft", {"encoder_out": -230}),
    ("end bell screws out", {f"bell_screw_{k}_out": -25 for k in range(1, 5)}),
    ("end bell + rear bearing + standoffs off", {"end_bell_out": -200}),
    ("carrier + clamp ring + output bearing + planets + sun out the front",
     {"carrier_pull": 130, "sun_key": 130, "output_bearing_out": 130, "clamp_out": 130}),
    ("rotor out the back", {"rotor_pull": -150, "encoder_out": -80, "sun_key": 280}),
    ("stator out", {"stator_out": -100}),
    ("pedestal screws out (from below)", {f"mount_screw_{k}_out": -50 for k in range(1, 5)}),   # tips clear the base (y -88)
    ("lift off pedestal", {"pedestal_out": -70}),
]
