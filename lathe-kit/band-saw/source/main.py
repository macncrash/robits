"""Vertical metal-cutting band saw on a stand, driven by an unknown-machine joint actuator through a 5:1 belt
(the accessory catalogue).

A separate machine. A complete actuator (linked design, revision 36) sits on its pedestal on a hinged motor plate
on the stand, axis front-to-back, and drives the lower band wheel through an HTD 8M 20T/100T timing belt (5:1).
The drive sets the blade speed anywhere from 0 to 166 m/min (wheel 0-212 rpm): about 30-40 m/min for mild steel,
20 for stainless, 100-150 for aluminium and brass, with no step pulleys or gearbox. The wheel gets about 50 N m
continuous (89 N m short-term), so about 400 N of blade pull: 270 W at 40 m/min, more than a 1/2 hp 4x6 saw puts
into its blade.

- Ø250 wheels with urethane tyres, 1829 mm (72 in) x 6-13 mm bi-metal blade; throat 280 mm, 100 mm under the
  guide.
- C-frame with the column on the right; idler wheel on a tension slider (screw, spring stack, scale for 6/10/13
  mm blades) with a tracking screw.
- Upper guide on a sliding post (lock knob, height scale in mm), lower guide under the table; bronze side blocks
  and a thrust face.
- 300 x 300 table, tilting 0-45 degrees left side down on two trunnions (engraved scale, knob pointer), miter
  slot and gauge.
- Wheel covers, chip brush, belt guard; welded stand, table top at 1000 mm.

Frame: the blade's cutting run is vertical at x 0, y 0, teeth toward the operator at -Y; the wheels turn in the
XZ plane about centres at x 125; the table top is z 0; Z up. The actuator, modelled with its axis along +Z and its
pedestal toward -Y, is turned 180 degrees about (0, 1, 1): its axis -> +Y (output to the back), its up -> Z.
"""
from steve import Design
from bandsaw_params import lower_z, upper_z, motor_y, motor_z
from links import actuator
from components.stand import stand
from components.motor_plate import motor_plate
from components.frame import frame
from components.lower_wheel import lower_wheel
from components.upper_wheel import upper_wheel
from components.lower_tyre import lower_tyre
from components.upper_tyre import upper_tyre
from components.blade import blade
from components.tension_slider import tension_slider
from components.drive_pulley import drive_pulley
from components.driven_pulley import driven_pulley
from components.belt import belt
from components.belt_guard import belt_guard
from components.upper_guide import upper_guide
from components.lower_guide import lower_guide
from components.trunnions import trunnions
from components.table import table
from components.miter_gauge import miter_gauge
from components.wheel_covers import wheel_covers

TURN = ((125, motor_y, motor_z), ((0, 1, 1), 180))   # actuator frame -> saw frame

design = Design("Vertical band saw (unknown-machine actuator, 5:1 belt) on stand")
design.add(actuator(), at=TURN, name="headstock")
for part in (stand, motor_plate, frame, lower_wheel, upper_wheel, lower_tyre, upper_tyre, blade, tension_slider, drive_pulley,
             driven_pulley, belt, belt_guard, upper_guide, lower_guide, trunnions, table, miter_gauge, wheel_covers):
    design.add(part)

# --- Motion ---
design.revolute("pulley_spin", "headstock", "drive_pulley", axis=((125, 0, motor_z), (0, 1, 0)))
design.revolute("lower_spin", "frame", "lower_wheel", axis=((125, 0, lower_z), (0, 1, 0)))
design.revolute("upper_spin", "tension_slider", "upper_wheel", axis=((125, 0, upper_z), (0, 1, 0)))
design.couple("blade_drive", {"pulley_spin": 5, "lower_spin": 1, "upper_spin": 1})   # 5:1 belt, equal wheels
design.rigid("pulley_keyed", "lower_wheel", "driven_pulley")
design.rigid("lower_tyre_on", "lower_wheel", "lower_tyre")
design.rigid("upper_tyre_on", "upper_wheel", "upper_tyre")
design.rigid("motor_plate_hinge", "stand", "motor_plate")
design.rigid("frame_bolts", "stand", "frame")
design.rigid("tension_set", "frame", "tension_slider")
design.rigid("blade_on_wheels", "frame", "blade")
design.rigid("belt_on_pulleys", "frame", "belt")
design.rigid("guard_tabs", "frame", "belt_guard")
design.rigid("covers_hinged", "frame", "wheel_covers")
design.rigid("lower_guide_bolts", "frame", "lower_guide")
design.rigid("trunnion_bolts", "frame", "trunnions")
design.slider("guide_height", "frame", "upper_guide", axis="Z", limits=(-50, 45))
design.revolute("table_tilt", "trunnions", "table", axis=((0, 0, 0), (0, 1, 0)), limits=(-45, 0))
design.slider("miter_slide", "table", "miter_gauge", axis="Y", limits=(-50, 60))

design.pose("bevel_45", table_tilt=-45)
design.pose("full_height", guide_height=45)
design.animation("cut", [({"blade_drive": 0, "miter_slide": -50, "guide_height": 0}, 0),
                         ({"blade_drive": 360, "miter_slide": -50}, 2),
                         ({"blade_drive": 1440, "miter_slide": 40}, 8),
                         ({"blade_drive": 1800, "miter_slide": -50}, 10)], loop=True)

# --- Designed contacts; everything else must not touch ---
for a, b in [("headstock", "motor_plate"), ("motor_plate", "stand"), ("frame", "stand"),
             ("drive_pulley", "headstock"), ("driven_pulley", "lower_wheel"), ("lower_tyre", "lower_wheel"),
             ("upper_tyre", "upper_wheel"), ("blade", "lower_tyre"), ("blade", "upper_tyre"), ("tension_slider", "frame"), ("lower_guide", "frame"),
             ("trunnions", "frame"), ("table", "trunnions"), ("miter_gauge", "table"), ("wheel_covers", "frame"),
             ("belt_guard", "frame")]:
    design.contact(a, b, kind="seated")
design.fit_check("fit", motion=False, poses=["bevel_45", "full_height"])

result = design.result()
