"""Cold saw on a stand, driven by a third unknown-machine joint actuator through a 20:1 worm gearbox (the shop
catalogue). A separate machine, not a lathe attachment.

A cold saw cuts steel with a slow HSS blade: Ø250 wants 30-40 m/min, about 45 rpm. The actuator alone gives
10 N m continuous, only about 47 W at 45 rpm, so a bought NMRV063 worm gearbox (i = 20, like a commercial cold
saw's) follows it: the actuator runs at about 900 rpm (about 0.94 kW continuous) and the blade gets about 45 rpm
and 150 N m (worm about 75 % efficient), about 1.2 kN at the teeth. The drive sets 0-53 rpm at the blade.

- Head: actuator on its pedestal on the head plate, jaw coupling to the worm's input, blade on an arbor through
  the gearbox's hollow output; fixed upper guard, moving lower guard, handle with a trigger.
- Chop pivot at the back on a Ø16 pin with return springs; the head swings for mitres on a turntable, 45 degrees
  either way, read on an engraved degree scale.
- Fence and quick-action vise on the base, length stop, chip and coolant tray, coolant tank and pump on the shelf.
- Welded stand, work table at 930 mm (stand top 900).

Frame: stock along X, blade in the YZ plane at x 0, operator at -Y, Z up, stand top at z 0, modelled with the head
down at the end of a cut. The actuator, modelled with its axis along +Z and its pedestal toward -Y, is turned 90
degrees about X (its axis -> -Y, toward the gearbox; its pedestal -> down).
"""
from steve import Design
from coldsaw_params import gear_x, worm_z, act_y, blade_y, blade_z, pivot_y, pivot_z, ratio
from links import actuator
from components.stand import stand
from components.chip_tray import chip_tray
from components.coolant_tank import coolant_tank
from components.base import base_c as base
from components.turntable import turntable
from components.pivot_pin import pivot_pin
from components.head_plate import head_plate
from components.gearbox import gearbox
from components.drive_hub import drive_hub
from components.coupling import coupling
from components.arbor import arbor_c as arbor
from components.blade import blade_c as blade
from components.outer_flange import outer_flange
from components.upper_guard import upper_guard
from components.lower_guard import lower_guard
from components.handle import handle
from components.fence import fence
from components.vise_jaw import vise_jaw
from components.vise_screw import vise_screw
from components.length_stop import length_stop
from components.stock import stock

TURN = ((gear_x, act_y, worm_z), ("X", 90))           # actuator frame -> saw frame

design = Design("Cold saw (unknown-machine actuator, worm reduction) on stand")
design.add(actuator(), at=TURN, name="headstock")
for part in (stand, chip_tray, coolant_tank, base, turntable, pivot_pin, head_plate, gearbox, drive_hub, coupling,
             arbor, blade, outer_flange, upper_guard, lower_guard, handle, fence, vise_jaw, vise_screw,
             length_stop, stock):
    design.add(part)

# --- Motion ---
design.revolute("mitre", "base", "turntable", axis=((0, 0, 0), (0, 0, 1)), limits=(-45, 45))
design.rigid("pin_in_cheeks", "turntable", "pivot_pin")
design.revolute("chop", "turntable", "head_plate", axis=((0, pivot_y, pivot_z), (1, 0, 0)), limits=(-35, 0))
design.rigid("motor_on_head", "head_plate", "headstock")
design.rigid("gearbox_on_head", "head_plate", "gearbox")
design.rigid("guard_on_gearbox", "gearbox", "upper_guard")
design.rigid("handle_on_gearbox", "gearbox", "handle")
design.revolute("motor_spin", "headstock", "drive_hub", axis=((gear_x, 0, worm_z), (0, -1, 0)))
design.rigid("coupling_on_hub", "drive_hub", "coupling")
design.revolute("blade_spin", "gearbox", "arbor", axis=((0, blade_y, blade_z), (-1, 0, 0)))
design.couple("drive", {"motor_spin": 1, "blade_spin": -1 / ratio})
design.rigid("blade_on_arbor", "arbor", "blade")
design.rigid("flange_nut", "arbor", "outer_flange")
design.revolute("lower_guard_swing", "upper_guard", "lower_guard", axis=((0, blade_y, blade_z), (1, 0, 0)),
                limits=(0, 95))
design.rigid("fence_bolts", "base", "fence")
design.slider("vise_travel", "base", "vise_jaw", axis="Y", limits=(-60, 0))
design.rigid("screw_in_jaw", "vise_jaw", "vise_screw")
design.slider("stop_set", "base", "length_stop", axis="X", limits=(-40, 60))
design.rigid("stock_clamped", "base", "stock")
design.rigid("tray_on_stand", "stand", "chip_tray")
design.rigid("tank_on_shelf", "stand", "coolant_tank")
design.rigid("base_bolts", "stand", "base")

design.pose("raised", chop=-35, lower_guard_swing=95)
design.pose("mitre_left", mitre=45, chop=-35, lower_guard_swing=95)
design.pose("mitre_right", mitre=-45, chop=-35, lower_guard_swing=95)
design.animation("chop", [({"chop": -35, "lower_guard_swing": 95, "motor_spin": 0}, 0),
                          ({"chop": -14, "lower_guard_swing": 60, "motor_spin": 3600}, 1.5),
                          ({"chop": 0, "lower_guard_swing": 0, "motor_spin": 14400}, 5),
                          ({"chop": 0, "lower_guard_swing": 0, "motor_spin": 16200}, 5.5),
                          ({"chop": -35, "lower_guard_swing": 95, "motor_spin": 18000}, 7)], loop=True)

# --- Designed contacts; everything else must not touch ---
for a, b in [("headstock", "head_plate"), ("drive_hub", "headstock"), ("coupling", "drive_hub"),
             ("coupling", "gearbox"), ("gearbox", "head_plate"), ("arbor", "gearbox"), ("blade", "arbor"),
             ("outer_flange", "blade"), ("outer_flange", "arbor"), ("upper_guard", "gearbox"), ("handle", "gearbox"),
             ("head_plate", "pivot_pin"), ("turntable", "pivot_pin"), ("turntable", "base"), ("base", "stand"),
             ("chip_tray", "stand"), ("coolant_tank", "stand"), ("fence", "base"), ("vise_jaw", "base"),
             ("vise_screw", "vise_jaw"), ("vise_screw", "base"), ("length_stop", "base"), ("stock", "base"),
             ("stock", "turntable"), ("stock", "fence"), ("stock", "vise_jaw"), ("stock", "length_stop")]:
    design.contact(a, b, kind="seated")
design.fit_check("fit", motion=False, poses=["raised", "mitre_left", "mitre_right"])

result = design.result()
