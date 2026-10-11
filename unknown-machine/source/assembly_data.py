"""Teardown order (service sequence) and the flange screw pattern."""
SCREW_PCD = 100  # mm Flange screw pitch circle
SCREW_ANGLES = (45, 135, 225, 315)  # degrees

STAGES = [
    ("open clamp lever", {"lever_pivot": 95}),
    ("flange screws out", {f"screw_{k}_out": 90 for k in range(1, 5)}),
    ("front flange off", {"flange_out": 70}),
    ("carrier + planets out", {"carrier_pull": 130}),
    ("ring gear out", {"ring_out": 95}),
    ("output bearing out", {"output_bearing_out": 70}),
    ("clamp band off the back", {"band_out": -135}),
    ("encoder cap off", {"cap_out": -270}),
    ("encoder disk off", {"encoder_out": -300}),
    ("end bell + rear bearing off", {"end_bell_out": -200}),
    ("rotor + sun out", {"rotor_pull": -150}),
    ("stator + windings out", {"stator_out": -100}),
    ("lift off pedestal", {"pedestal_out": -70}),
]
