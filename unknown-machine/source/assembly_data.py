"""Teardown order (service sequence) and the flange screw pattern."""
SCREW_PCD = 100  # mm Flange screw pitch circle
SCREW_ANGLES = (45, 135, 225, 315)  # degrees

# Order checked with the animation's collision sweep: the ring gear is pressed into the flange (they come off
# together, then it is pressed out forward); the sun is caught inside the carrier, so it slides off the shaft and
# comes out with the carrier before the rotor goes out the back; the encoder disk and the sun ride on the rotor,
# so their slides back off while the rotor is pulled (their positions stay put).
STAGES = [
    ("flange screws out", {f"screw_{k}_out": 90 for k in range(1, 5)}),
    ("front flange + ring gear off", {"flange_out": 70, "ring_out": 70}),
    ("ring gear pressed out of the flange", {"ring_out": 95}),
    ("encoder cap off", {"cap_out": -270}),
    ("encoder disk off", {"encoder_out": -230}),
    ("end bell + rear bearing off", {"end_bell_out": -200}),
    ("carrier + planets + sun out the front", {"carrier_pull": 130, "sun_key": 130}),
    ("output bearing out", {"output_bearing_out": 70}),
    ("rotor out the back", {"rotor_pull": -150, "encoder_out": -80, "sun_key": 280}),
    ("stator out", {"stator_out": -100}),
    ("pedestal screws out (from below)", {f"mount_screw_{k}_out": -50 for k in range(1, 5)}),   # tips clear the base (y -88)
    ("lift off pedestal", {"pedestal_out": -70}),
]
