"""Crawler transporter.

Read from the sheet: a black tracked transporter, cab forward, long riveted
hull, bumper, roof rails, a raised bay on the deck, a side hatch and a
ladder. Built as a two-crew cargo crawler. The shoe bands are rigid envelopes.
The sprockets, idlers and road wheels turn inside them.

The robits joint actuator is a 2 N·m module. Each sprocket here wants a few
thousand N·m. This machine does not use that module. The motors are the
final-drive housings; requirements/motor.toml is the check against the
frameless cards.

Frame: X forward, Y to the left, Z up. Origin on the ground, mid-length.
"""
from steve import Design
from params import (
    center_z, door_deg, door_x, door_y, door_z, idler_r, ix, pitch_r, sx,
    track_y, wheel_r, wheel_xs, wheel_z,
)
from components.hull import hull
from components.track import track
from components.sprocket import sprocket
from components.idler import idler
from components.road_wheel import road_wheel
from components.door import door

design = Design("Crawler transporter")
design.add(hull)

for side, y in (("l", track_y), ("r", -track_y)):
    design.add(track, name=f"track_{side}", at=(0, y, 0))
    design.add(idler, name=f"idler_{side}", at=(ix, y, center_z))
    for n, x in enumerate(wheel_xs):
        design.add(road_wheel, name=f"wheel_{side}{n}", at=(x, y, wheel_z))

design.add(sprocket, name="sprocket_l", at=(sx, track_y, center_z))
design.add(sprocket, name="sprocket_r", at=((sx, -track_y, center_z), ("Z", 180)))
design.add(door, name="door_l", at=(door_x, door_y, door_z))
design.add(door, name="door_r", at=(door_x, -door_y, door_z))

# Positive about +Y drives the contact patch rearward, so the crawler goes forward.
for side, y in (("l", track_y), ("r", -track_y)):
    design.revolute(
        f"sprocket_{side}", "hull", f"sprocket_{side}",
        axis=((sx, y, center_z), (0, 1, 0)),
    )
    design.revolute(
        f"idler_{side}", "hull", f"idler_{side}",
        axis=((ix, y, center_z), (0, 1, 0)),
        follow=True,
    )
    for n, x in enumerate(wheel_xs):
        design.revolute(
            f"wheel_{side}{n}", "hull", f"wheel_{side}{n}",
            axis=((x, y, wheel_z), (0, 1, 0)),
            follow=True,
        )
    design.rigid(f"track_on_{side}", "hull", f"track_{side}")

design.revolute("door_l", "hull", "door_l", axis=((door_x, door_y, door_z), (0, 0, 1)), limits=(-door_deg, 0))
design.revolute("door_r", "hull", "door_r", axis=((door_x, -door_y, door_z), (0, 0, 1)), limits=(0, door_deg))

k_w = pitch_r / wheel_r
k_i = pitch_r / idler_r
roll = {}
skid = {}
for side, sign in (("l", 1.0), ("r", -1.0)):
    roll[f"sprocket_{side}"] = 1.0
    skid[f"sprocket_{side}"] = sign
    roll[f"idler_{side}"] = k_i
    skid[f"idler_{side}"] = sign * k_i
    for n in range(len(wheel_xs)):
        roll[f"wheel_{side}{n}"] = k_w
        skid[f"wheel_{side}{n}"] = sign * k_w

design.couple("roll", roll)
design.couple("skid", skid, limits=(-40, 40))

design.pose("board", door_l=-door_deg, door_r=door_deg)
design.pose("pivot", skid=30)
design.animation(
    "crawl",
    [({"roll": 0}, 0), ({"roll": 360}, 8)],
    loop=True,
)

design.fit_check("fit", motion=False, poses=["board"])

result = design.result()
