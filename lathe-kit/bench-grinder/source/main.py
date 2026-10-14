"""Bench grinder (unknown-machine motor, direct drive) on a pedestal stand.

A separate machine from the lathe, built round the same Kollmorgen KBM-17H01-B00 frameless motor and the same
240 Vac servo drive, but with no gearbox: the 5:1 actuator's 1060 rpm is far too slow for vitrified wheels.
The drive's speed limit is set to 3450 rpm, which gives 27 m/s on Ø150 wheels (rated 35 m/s, 4140 rpm or more).

- Head: one 42CrMo4 through-shaft on two 6204-2RS bearings in 6061 end bells, the KBM rotor bonded on it and the
  stator bonded in a 6061 barrel. A Ø150 x 20 wheel at each end (A36 coarse on the left, WA80 white on the
  right), clamped between Ø60 flanges by M20 x 1.5 nuts (left-hand thread on the left).
- Cast guards opened only from 10 degrees below to 65 degrees above the horizontal, spark deflectors 3 mm off the
  wheel, tool rests 2 mm off it at the wheel centre, polycarbonate eye shields.
- Head foot bolted to a welded pedestal stand: base plate for floor bolts, Ø101.6 column, top plate, gussets.
  Spindle at 1020 mm. Optional quench pot on the column; drive box with start and e-stop on the front.

Frame: spindle along X at y 0, z 1020; Z up from the floor; operator at -Y. Parts that come in pairs are
modelled on the right and turned 180 degrees about Z (or mirrored in their component) for the left.
"""
from steve import Design
from grinder_params import spindle_z
from components.shaft import shaft
from components.motor_rotor import motor_rotor
from components.stator import stator
from components.barrel import barrel
from components.end_bell import end_bell
from components.bearing_6204 import bearing_6204
from components.spacer import spacer
from components.wheel_flange import wheel_flange
from components.shaft_nut import shaft_nut
from components.wheel_coarse import wheel_coarse
from components.wheel_fine import wheel_fine
from components.wheel_guards import wheel_guards
from components.tool_rests import tool_rests
from components.eye_shields import eye_shields
from components.head_foot import head_foot
from components.pedestal_stand import pedestal_stand
from components.quench_pot import quench_pot
from components.drive_box import drive_box

LEFT = ((0, 0, 0), ("Z", 180))                        # right-hand part turned onto the left

design = Design("Bench grinder (unknown-machine motor, direct drive) on pedestal stand")
for part in (shaft, motor_rotor, stator, barrel, wheel_guards, tool_rests, eye_shields, head_foot, pedestal_stand,
             quench_pot, drive_box):
    design.add(part)
for part, name in ((end_bell, "end_bell"), (bearing_6204, "bearing"), (spacer, "spacer"), (shaft_nut, "nut")):
    design.add(part, name=f"{name}_right")
    design.add(part, at=LEFT, name=f"{name}_left")
design.add(wheel_flange, name="flange_inner_right")
design.add(wheel_flange, at=LEFT, name="flange_inner_left")
design.add(wheel_flange, at=((250, 0, 0), ("Z", 180)), name="flange_outer_right")
design.add(wheel_flange, at=(-250, 0, 0), name="flange_outer_left")
design.add(wheel_fine, name="wheel_right")
design.add(wheel_coarse, at=LEFT, name="wheel_left")

# --- Motion: the spindle and everything clamped on it turns in the barrel's bearings ---
design.revolute("spindle", "barrel", "shaft", axis=((0, 0, spindle_z), (1, 0, 0)))
for part in ("motor_rotor", "spacer_right", "spacer_left", "flange_inner_right", "flange_inner_left",
             "flange_outer_right", "flange_outer_left", "wheel_right", "wheel_left", "nut_right", "nut_left"):
    design.rigid(f"{part}_on_shaft", "shaft", part)
design.animation("spin_up", [({"spindle": 0}, 0), ({"spindle": 360}, 1), ({"spindle": 1800}, 3),
                             ({"spindle": 3600}, 5)], easing="linear")

# --- Designed contacts; everything else must not touch ---
for a, b in [("stator", "barrel"), ("motor_rotor", "shaft"), ("end_bell_*", "barrel"), ("bearing_*", "shaft"),
             ("bearing_*", "end_bell_*"), ("spacer_*", "shaft"), ("spacer_*", "bearing_*"),
             ("flange_*", "shaft"), ("flange_inner_*", "spacer_*"), ("wheel_*", "shaft"), ("wheel_*", "flange_*"),
             ("nut_*", "shaft"), ("nut_*", "flange_outer_*"), ("wheel_guards", "end_bell_*"),
             ("tool_rests", "wheel_guards"), ("eye_shields", "wheel_guards"), ("barrel", "head_foot"),
             ("head_foot", "pedestal_stand"), ("quench_pot", "pedestal_stand"), ("drive_box", "pedestal_stand")]:
    design.contact(a, b, kind="seated")
design.fit_check("fit", motion=False)

result = design.result()
