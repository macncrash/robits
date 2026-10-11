"""Unknown machine – planetary joint actuator

A guess at what the AI "unknown machine" image (thisone.png) would be if it were real: a compact robot-joint
actuator. Reading the outside features as a design intent:
- finned can = frameless BLDC motor (stator, windings, magnet rotor on a hollow shaft);
- toothed ring in the front recess = fixed ring gear of a planetary stage; the disk inside it is the planet
  carrier (the output) and the small hub with a bore is the output with a hollow cable pass-through;
- knurled rear cap = encoder cover (encoder disk + read head on the end bell);
- stainless band + top lever = quick-release cam clamp that holds the actuator in the pedestal saddle.

Joints: the motor drives the gear train (coupling "spin", ratio 1 + ring/sun). Every part also has a slide
joint so the animation "teardown" takes it apart in a service order; pose "exploded" shows it fully apart.
Axis along +Z, output face at +Z, pedestal toward -Y. Parameters: params.py.
"""
import math

from steve import Design
from params import sun_teeth, planet_teeth
from assembly_data import STAGES, SCREW_ANGLES, SCREW_PCD
from components.housing import housing
from components.end_bell import end_bell
from components.rear_cap import rear_cap
from components.encoder_disk import encoder_disk
from components.read_head import read_head
from components.rear_bearing import rear_bearing
from components.stator import stator
from components.windings import windings
from components.rotor import rotor
from components.sun import sun
from components.carrier import carrier, orbit
from components.needle_bearing import needle_bearing
from components.planet import planet
from components.ring_gear import ring_gear, ring_teeth
from components.output_bearing import output_bearing
from components.front_flange import front_flange
from components.flange_screw import flange_screw
from components.clamp_band import clamp_band
from components.lever import lever
from components.pedestal import pedestal

gear_z = 48  # Gear stage starts here (mm along the axis)

design = Design("Unknown machine – planetary joint actuator")
for part in (housing, end_bell, rear_cap, encoder_disk, read_head, rear_bearing, stator, windings, rotor,
             sun, carrier, needle_bearing, ring_gear, output_bearing, front_flange, clamp_band, lever, pedestal):
    design.add(part)
for k in range(3):
    angle = 120 * k
    # Turned so its teeth fall into the sun's gaps (Zs + Zr divisible by 3 keeps the ring meshing too).
    phase = angle + 180 - 180 / planet_teeth + angle * sun_teeth / planet_teeth
    centre = (orbit * math.cos(math.radians(angle)), orbit * math.sin(math.radians(angle)), gear_z)
    design.add(planet, at=(centre, ("Z", phase)), name=f"planet_{k + 1}")
for k, a in enumerate(SCREW_ANGLES):
    r = SCREW_PCD / 2
    design.add(flange_screw, at=(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)), 59.5),
               name=f"screw_{k + 1}")

# --- Working joints: motor -> sun -> planets -> carrier (ring gear fixed in the flange) ---
carrier_ratio = sun_teeth / (sun_teeth + ring_teeth)
planet_ratio = -(sun_teeth / planet_teeth) * (1 - carrier_ratio)
design.cylindrical("rotor_axis", "housing", "rotor", axis="Z", slide_limits=(-160, 0))
design.rigid("sun_key", "rotor", "sun")
design.slider("encoder_out", "rotor", "encoder_disk", axis="Z", limits=(-310, 0))
design.cylindrical("carrier_axis", "housing", "carrier", axis="Z", slide_limits=(0, 140))
design.rigid("needle_fit", "carrier", "needle_bearing")
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

# --- Clamp lever on the band ---
design.revolute("lever_pivot", "clamp_band", "lever", axis=((0, 68, 26), (1, 0, 0)), limits=(0, 100))

# --- Teardown slides (0 = assembled) ---
design.slider("band_out", "housing", "clamp_band", axis="Z", limits=(-140, 0))
design.slider("pedestal_out", "housing", "pedestal", axis="Y", limits=(-80, 0))
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
design.rigid("windings_in_stator", "stator", "windings")

# Teardown: each stage keeps what the stages before it moved.
design.pose("assembled", lever_pivot=0)
keys, values = [("assembled", 0)], {}
for i, (stage, moves) in enumerate(STAGES):
    values = {**values, **moves}
    keys.append((dict(values), i + 1))
design.pose("exploded", **values)
design.animation("teardown", keys + [(dict(values), len(STAGES) + 1.5)], loop=False, easing="ease")

# Designed contacts (seats, press fits, gear meshes, threads); everything else must not touch.
for a, b in [("rear_bearing", "end_bell"), ("rear_bearing", "rotor"), ("output_bearing", "housing"),
             ("output_bearing", "carrier"), ("needle_bearing", "carrier"), ("stator", "housing"),
             ("windings", "stator"), ("sun", "rotor"), ("encoder_disk", "rotor"), ("sun", "planet_*"),
             ("planet_*", "ring_gear"), ("ring_gear", "front_flange"), ("front_flange", "housing"),
             ("screw_*", "front_flange"), ("end_bell", "housing"), ("rear_cap", "end_bell"),
             ("read_head", "end_bell"), ("clamp_band", "housing")]:
    design.contact(a, b, kind="seated")
design.contact("screw_*", "housing", kind="threaded")
design.fit_check("fit", motion=False)

result = design.result()
