"""Unknown machine – planetary joint actuator

A guess at what the AI "unknown machine" image (thisone.png) would be if it were real: a compact robot-joint
actuator. Reading the outside features as a design intent:
- finned can = frameless BLDC motor (stator, windings, magnet rotor on a hollow shaft);
- toothed ring in the front recess = fixed ring gear of a planetary stage; the disk inside it is the planet
  carrier (the output) and the small hub with a bore is the output with a hollow cable pass-through;
- knurled rear cap = encoder cover (encoder disk + read head on the end bell);
- stainless band + top lever = a quick-release cam clamp in the image. It was dropped: the housing now sits
  straight in the pedestal saddle on a thermal pad (the pedestal is its heat sink), held by 4 x M5 x 20 screws
  from below and located by 2 x 4 mm dowels.
Screw joints are declared with design.fasten and checked every build (engagement, bottoming, walls); threads in
the aluminium housing get at least 2.2 d of engagement (rule set to 2 d: conservative for 6061-T6 with A2-70).

Joints: the motor drives the gear train (coupling "spin", ratio 1 + ring/sun). Every part also has a slide
joint so the animation "teardown" takes it apart in a service order; pose "exploded" shows it fully apart.
Axis along +Z, output face at +Z, pedestal toward -Y. Parameters: params.py.
"""
import math

from steve import Design
from params import sun_teeth, planet_teeth, module

orbit = module * (sun_teeth + planet_teeth) / 2  # Planet centres
from assembly_data import STAGES, SCREW_ANGLES, SCREW_PCD
from components.housing import housing
from components.end_bell import end_bell
from components.rear_cap import rear_cap
from components.encoder_disk import encoder_disk
from components.read_head import read_head
from components.stator import stator
from components.motor_rotor import motor_rotor
from components.rotor import rotor
from components.sun import sun
import params
from links import carrier
carrier = carrier(module=params.module, sun_teeth=params.sun_teeth, planet_teeth=params.planet_teeth)
from links import carrier_disk   # carrier is two pieces: rear part with posts + this bolted front disk / output hub
carrier_disk = carrier_disk(module=params.module, sun_teeth=params.sun_teeth, planet_teeth=params.planet_teeth)
from components.needle_bearing import needle_bearing
from components.planet import planet
from components.planet_needle import planet_needle
from components.ring_gear import ring_gear, ring_teeth
from components.output_bearing import output_bearing
from components.front_flange import front_flange
from components.mount_dowel import mount_dowel
from links import pedestal
pedestal = pedestal()
from components.bearing_6001_2rs_sealed_simple import bearing_6001_2rs_sealed_simple
from components.planet_pin import planet_pin
from components.iso4762_socket_head_cap_screw_m5x20 import iso4762_socket_head_cap_screw_m5x20
from components.iso4762_socket_head_cap_screw_m5x30 import iso4762_socket_head_cap_screw_m5x30
from components.countersunk_socket_screw_m4_l0016_simple import countersunk_socket_screw_m4_l0016_simple   # A2-70

gear_z = 48  # Gear stage starts here (mm along the axis)

design = Design("Unknown machine – planetary joint actuator")
for part in (housing, end_bell, rear_cap, encoder_disk, read_head, stator, motor_rotor, rotor,
             sun, carrier, carrier_disk, needle_bearing, ring_gear, output_bearing, front_flange, pedestal):
    design.add(part)
for k in range(3):
    angle = 120 * k
    # Turned so its teeth fall into the sun's gaps (Zs + Zr divisible by 3 keeps the ring meshing too).
    phase = angle + 180 - 180 / planet_teeth + angle * sun_teeth / planet_teeth
    centre = (orbit * math.cos(math.radians(angle)), orbit * math.sin(math.radians(angle)), gear_z)
    design.add(planet, at=(centre, ("Z", phase)), name=f"planet_{k + 1}")
    design.add(planet_needle, at=(centre, ("Z", phase)), name=f"needle_p{k + 1}")
# Catalog parts (step.parts): rear bearing 6001-2RS, 4x ISO 4762 M5x30 flange screws (14.5 mm into the housing). Planet pins are ISO 2338
# 6x18 dowels, modelled (the catalog's dowel-pin files are twice their nominal length).
design.add(bearing_6001_2rs_sealed_simple, at=(0, 0, -46), name="rear_bearing")
for k, a in enumerate(SCREW_ANGLES):
    r = SCREW_PCD / 2
    design.add(iso4762_socket_head_cap_screw_m5x30,
               at=(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), 59.5), name=f"screw_{k + 1}")
for k in range(3):
    a = math.radians(120 * k)
    design.add(planet_pin, at=(orbit * math.cos(a), orbit * math.sin(a), 44.5), name=f"pin_{k + 1}")
# Front disk screws: ISO 10642 M4x16 countersunk (step.parts, origin on the head's top face) into the bridge posts,
# heads flush with the disk face (z 65.5) in 9.0 mm countersinks; 11 mm of thread in each post.
for k in range(3):
    a = math.radians(120 * k + 60)
    design.add(countersunk_socket_screw_m4_l0016_simple, at=(orbit * math.cos(a), orbit * math.sin(a), 65.5),
               name=f"disk_screw_{k + 1}")
# Pedestal mount: ISO 4762 M5 x 20 from below (step.parts, origin under the head), heads on the counterbore floor
# at y -66, about 11 mm of thread in the housing (its surface is at y -57.8 at x = 16); two ISO 2338 4 x 12 dowels.
for k, (x, z) in enumerate((x, z) for z in (28, 37) for x in (-16, 16)):
    design.add(iso4762_socket_head_cap_screw_m5x20, at=((x, -66, z), ("X", 90)), name=f"mount_screw_{k + 1}")
for k, z in enumerate((22, 40)):
    design.add(mount_dowel, at=(0, -66, z), name=f"mount_dowel_{k + 1}")

# --- Working joints: motor -> sun -> planets -> carrier (ring gear fixed in the flange) ---
carrier_ratio = sun_teeth / (sun_teeth + ring_teeth)
planet_ratio = -(sun_teeth / planet_teeth) * (1 - carrier_ratio)
design.cylindrical("rotor_axis", "housing", "rotor", axis="Z", slide_limits=(-160, 0))
design.slider("sun_key", "rotor", "sun", axis="Z", limits=(0, 300))   # keyed; slides off the shaft nose forward
design.slider("encoder_out", "rotor", "encoder_disk", axis="Z", limits=(-310, 0))
design.cylindrical("carrier_axis", "housing", "carrier", axis="Z", slide_limits=(0, 140))
design.rigid("needle_fit", "carrier", "needle_bearing")
design.rigid("disk_bolted", "carrier", "carrier_disk")   # 3 x M4 countersunk screws, located by the planet pins
for k in range(3):
    design.rigid(f"disk_screw_fit_{k + 1}", "carrier_disk", f"disk_screw_{k + 1}")
for k in range(3):
    design.rigid(f"pin_fit_{k + 1}", "carrier", f"pin_{k + 1}")
    design.rigid(f"needle_p_fit_{k + 1}", f"planet_{k + 1}", f"needle_p{k + 1}")   # cup pressed in the planet
for k in range(3):
    a = math.radians(120 * k)
    design.revolute(f"planet_spin_{k + 1}", "carrier", f"planet_{k + 1}",
                    axis=((orbit * math.cos(a), orbit * math.sin(a), gear_z), (0, 0, 1)))
design.couple("spin", {"rotor_axis.turn": 1, "carrier_axis.turn": carrier_ratio,
                       "planet_spin_1": planet_ratio, "planet_spin_2": planet_ratio, "planet_spin_3": planet_ratio})
design.drive("spin", speed=360)
# Pulls for the two turning parts (their slide), used by the teardown.
design.couple("rotor_pull", {"rotor_axis.travel": 1}, limits=(-160, 0))
design.couple("carrier_pull", {"carrier_axis.travel": 1}, limits=(0, 140))

# --- Teardown slides (0 = assembled) ---
design.slider("pedestal_out", "housing", "pedestal", axis="Y", limits=(-80, 0))
for k in range(1, 5):
    design.slider(f"mount_screw_{k}_out", "pedestal", f"mount_screw_{k}", axis="Y", limits=(-50, 0))
for k in range(1, 3):
    design.rigid(f"mount_dowel_fit_{k}", "pedestal", f"mount_dowel_{k}")   # pressed into the pedestal
design.slider("flange_out", "housing", "front_flange", axis="Z", limits=(0, 80))
for k in range(len(SCREW_ANGLES)):
    design.slider(f"screw_{k + 1}_out", "housing", f"screw_{k + 1}", axis="Z", limits=(0, 100))
design.slider("ring_out", "housing", "ring_gear", axis="Z", limits=(0, 100))
design.slider("output_bearing_out", "housing", "output_bearing", axis="Z", limits=(0, 80))
design.slider("cap_out", "housing", "rear_cap", axis="Z", limits=(-280, 0))
design.slider("end_bell_out", "housing", "end_bell", axis="Z", limits=(-210, 0))
design.rigid("rear_bearing_fit", "end_bell", "rear_bearing")
design.rigid("read_head_mount", "end_bell", "read_head")
design.slider("stator_out", "housing", "stator", axis="Z", limits=(-110, 0))
design.rigid("rotor_bonded", "rotor", "motor_rotor")   # KBM rotor bonded to the hub sleeve

# Teardown: each stage keeps what the stages before it moved.
design.pose("assembled", pedestal_out=0)
keys, values = [("assembled", 0)], {}
for i, (stage, moves) in enumerate(STAGES):
    values = {**values, **moves}
    keys.append((dict(values), i + 1))
design.pose("exploded", **values)
design.animation("teardown", keys + [(dict(values), len(STAGES) + 1.5)], loop=False, easing="ease", check=True)

# Designed contacts (seats, press fits, gear meshes, threads); everything else must not touch.
for a, b in [("rear_bearing", "end_bell"), ("rear_bearing", "rotor"), ("output_bearing", "housing"),
             ("output_bearing", "carrier"), ("needle_bearing", "carrier"), ("stator", "housing"),
             ("motor_rotor", "rotor"), ("sun", "rotor"), ("encoder_disk", "rotor"), ("sun", "planet_*"),
             ("planet_*", "ring_gear"), ("ring_gear", "front_flange"), ("front_flange", "housing"),
             ("screw_*", "front_flange"), ("end_bell", "housing"), ("rear_cap", "end_bell"),
             ("read_head", "end_bell"), ("pedestal", "housing"), ("pin_*", "carrier"),
             ("mount_screw_*", "pedestal"), ("mount_dowel_*", "pedestal"), ("mount_dowel_*", "housing")]:
    design.contact(a, b, kind="seated")
design.contact("carrier_disk", "carrier", kind="seated")
design.contact("pin_*", "carrier_disk", kind="seated")
design.contact("disk_screw_*", "carrier_disk", kind="seated")
design.contact("disk_screw_*", "carrier", kind="threaded")
for k in range(1, 4):
    design.contact(f"needle_p{k}", f"planet_{k}", kind="seated")
    design.contact(f"needle_p{k}", f"pin_{k}", kind="seated")
design.contact("screw_*", "housing", kind="threaded")
design.contact("mount_screw_*", "housing", kind="threaded")
design.fit_check("fit", motion=False)

# Declared screw joints: checked at every build on the geometry as built (inspect_model checks=["fasteners"]).
for k, a in enumerate(SCREW_ANGLES):
    r = SCREW_PCD / 2
    x, y = r * math.cos(math.radians(a)), r * math.sin(math.radians(a))
    design.fasten(f"flange_screw_{k + 1}", "ISO 4762 M5x30", axis=((x, y, 59.5), (0, 0, -1)),
                  clamps=["front_flange"], into="housing", thread="tapped", instance=f"screw_{k + 1}")
for k, (x, z) in enumerate((x, z) for z in (28, 37) for x in (-16, 16)):
    design.fasten(f"mount_screw_{k + 1}", "ISO 4762 M5x20", axis=((x, -66, z), (0, 1, 0)),
                  clamps=["pedestal"], into="housing", thread="tapped", instance=f"mount_screw_{k + 1}")
for k in range(3):
    a = math.radians(120 * k + 60)
    design.fasten(f"disk_screw_{k + 1}", "ISO 10642 M4x16", axis=((orbit * math.cos(a), orbit * math.sin(a), 65.5), (0, 0, -1)),
                  clamps=["carrier_disk"], into="carrier", thread="tapped", instance=f"disk_screw_{k + 1}")
design.fastener_rules(min_engagement_d=2.0)   # conservative for steel screws in aluminium / 303

result = design.result()
