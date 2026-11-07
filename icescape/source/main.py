"""Icescape ice rover.

Read from the shirt: a low wedge, four large open wheels, a glazed canopy, a light bar on the nose
and a small mast at the tail. Built as a four-wheel-steer, four-wheel-drive rover for Antarctic
sea ice and sastrugi, and for icy ground offworld (a lunar cold trap, the Martian polar cap).

Each corner is two of the robits joint actuators. One, axis vertical, steers. One, axis along the
axle, drives a second 5:1 planetary in the hub, 25:1 overall from the Kollmorgen KBM-17H01-C. The
linked part is the bare joint shell (pedestal off). The internals, the 5:1 stage and the torque
are the unknown-machine actuator.

Frame: X forward, Y to the left, Z up. Origin on the ice, midway between the axles.
"""
from steve import Design
from params import (
    act_diameter, act_length, half_track, half_wb, steer_deg, steer_y, steer_z, arm_deg,
    drive_y, wheel_r,
)
from links import actuator
from components.hull import hull
from components.arm import arm
from components.upright import upright
from components.hub import hub
from components.wheel import wheel

design = Design("Icescape ice rover")
design.add(hull)

CORNERS = (("lf", half_wb, half_track), ("rf", half_wb, -half_track),
           ("lr", -half_wb, half_track), ("rr", -half_wb, -half_track))

ACT = dict(diameter=act_diameter, length=act_length, pedestal=0, fin_count=9)


def world(local, x, y, right):
    lx, ly, lz = local
    if right:
        lx, ly = -lx, -ly
    return (x + lx, y + ly, wheel_r + lz)


for name, x, y in CORNERS:
    right = y < 0
    at = ((x, y, wheel_r), ("Z", 180)) if right else (x, y, wheel_r)
    design.add(arm, name=f"arm_{name}", at=at)
    design.add(upright, name=f"upright_{name}", at=at)
    design.add(hub, name=f"hub_{name}", at=at)
    design.add(wheel, name=f"wheel_{name}", at=at)
    design.add(
        actuator(**ACT),
        name=f"steer_{name}",
        at=(world((0, steer_y, steer_z), x, y, right), ("X", 180) if right else ("Y", 180)),
    )
    design.add(
        actuator(**ACT),
        name=f"drive_{name}",
        at=(world((0, drive_y, 0), x, y, right), ("X", 90) if right else ("X", -90)),
    )

for name, x, y in CORNERS:
    right = y < 0
    pivot = world((0, -300, 145), x, y, right)
    kingpin = world((0, steer_y, 0), x, y, right)
    axle = (x, y, wheel_r)
    # Positive swing about +X lifts the left wheels and drops the right ones.
    design.revolute(f"swing_{name}", "hull", f"arm_{name}", axis=(pivot, (1, 0, 0)), limits=(-arm_deg, arm_deg))
    design.revolute(f"yaw_{name}", "arm_" + name, f"upright_{name}", axis=(kingpin, (0, 0, 1)),
                    limits=(-steer_deg, steer_deg))
    design.revolute(f"spin_{name}", f"upright_{name}", f"hub_{name}", axis=(axle, (0, 1, 0)))
    design.rigid(f"wheel_on_{name}", f"hub_{name}", f"wheel_{name}")
    design.rigid(f"steer_on_{name}", f"arm_{name}", f"steer_{name}")
    design.rigid(f"drive_on_{name}", f"upright_{name}", f"drive_{name}")

design.pose("crab", yaw_lf=20, yaw_rf=20, yaw_lr=20, yaw_rr=20)
design.pose("bump", swing_lf=6, swing_lr=6, swing_rf=-6, swing_rr=-6)
design.animation(
    "traverse",
    [({"spin_lf": 0, "spin_rf": 0, "spin_lr": 0, "spin_rr": 0}, 0),
     ({"spin_lf": -360, "spin_rf": 360, "spin_lr": -360, "spin_rr": 360,
       "yaw_lf": 18, "yaw_rf": 18, "yaw_lr": -8, "yaw_rr": -8}, 6),
     ({"spin_lf": -720, "spin_rf": 720, "spin_lr": -720, "spin_rr": 720,
       "yaw_lf": 0, "yaw_rf": 0, "yaw_lr": 0, "yaw_rr": 0}, 12)],
    loop=True,
)

design.fit_check("fit", motion=False, poses=["crab", "bump"])

result = design.result()
