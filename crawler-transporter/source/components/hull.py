"""Hull, cab, bumper, keel, and the fixed running-gear frame.

The side profile matches the sheet: a long plate hull, a taller cab at the
front, a bumper ahead of the tracks, and the body sitting on top of the
track bands. The keel hangs between the tracks, where the side view cannot
see it, and carries the final drives.

Rivets in the drawing are the plate fasteners. The shell is the plate, with
no head at every hole.
"""
from steve import Component
from params import (
    bumper_bottom, bumper_front, bumper_top, cab_back, cab_roof, center_z,
    half_w, hull_bottom, hull_front, hull_rear, hull_roof, sx, track_y, wall,
    wheel_xs,
)

hull = Component("hull", name="Hull")

with hull.sketch("profile", on="XZ") as s:
    s.polyline("side", [
        (hull_rear, hull_bottom),
        (hull_front, hull_bottom),
        (hull_front, bumper_bottom),
        (bumper_front, bumper_bottom),
        (bumper_front, bumper_top),
        (hull_front, bumper_top),
        (hull_front, cab_roof),
        (cab_back, cab_roof),
        (cab_back, hull_roof),
        (hull_rear, hull_roof),
    ])
hull.extrude("skin", "profile", distance=2 * half_w, both=True)

with hull.sketch("inner", on="XZ") as s:
    s.polyline("void", [
        (hull_rear + wall, hull_bottom + wall),
        (hull_front - wall, hull_bottom + wall),
        (hull_front - wall, cab_roof - wall),
        (cab_back + wall, cab_roof - wall),
        (cab_back + wall, hull_roof - wall),
        (hull_rear + wall, hull_roof - wall),
    ])
hull.extrude("cavity", "inner", distance=2 * half_w - 2 * wall, both=True, op="cut")

# Rear step, above and behind the track.
hull.box("rear_step", 240, 1200, 520, at=(hull_rear - 100, 0, 1980), op="join")

# Cooling plenum on the rear roof. The throat opens into the bay.
hull.box("plenum", 1600, 800, 380, at=(-1400, 0, 2670), op="join")
hull.box("plenum_void", 1460, 660, 280, at=(-1400, 0, 2660), op="cut")
hull.box("plenum_throat", 500, 360, 80, at=(-1400, 0, 2490), op="cut")

# Deck rail along the hull roof, both sides, stopping short of the cab.
for side, y in (("l", 1180.0), ("r", -1180.0)):
    hull.box(f"rail_{side}", 3200, 28, 28, at=(-1200, y, 2640), op="join")
    for n, x in enumerate((-2700.0, -1900.0, -1100.0, -300.0)):
        hull.box(f"rail_post_{side}{n}", 24, 24, 160, at=(x, y, 2570), op="join")
hull.box("plenum_rail", 1200, 28, 28, at=(-1400, 0, 2960), op="join")
for n, x in enumerate((-1850.0, -950.0)):
    hull.box(f"plenum_post_{n}", 24, 24, 120, at=(x, 0, 2900), op="join")

# Ladder on the left side, aft of the cab. The drawing shows this side.
for n, x in enumerate((500.0, 640.0)):
    hull.box(f"stile_{n}", 22, 40, 1000, at=(x, 1248, 2000), op="join")
for n, z in enumerate((1620.0, 1820.0, 2020.0, 2220.0, 2420.0)):
    hull.box(f"rung_{n}", 162, 28, 16, at=(570, 1256, z), op="join")

# Mirrors at the cab's front corners.
for side, sign in (("l", 1.0), ("r", -1.0)):
    hull.box(f"mirror_{side}", 16, 200, 280, at=(2660, sign * 1380, 2680), op="join")
    hull.box(f"mirror_stalk_{side}", 36, 200, 36, at=(2660, sign * 1230, 2680), op="join")

# Keel between the tracks, a 16 mm box from 480 mm off the ground up into the floor.
hull.box("keel", 4800, 1280, 900, at=(-200, 0, 930), op="join")
hull.box("keel_void", 4768, 1248, 852, at=(-200, 0, 922), op="cut")

# Spine in each track loop, an arm over each road wheel, posts inboard to the keel.
for side, y in (("l", track_y), ("r", -track_y)):
    hull.box(f"spine_{side}", 2900, 100, 520, at=(-50, y, 840), op="join")
    for n, x in enumerate(wheel_xs):
        hull.box(f"arm_{side}{n}", 50, 36, 110, at=(x, y, 535), op="join")
    post_y = 700.0 if y > 0 else -700.0
    link_y = 820.0 if y > 0 else -820.0
    for n, x in enumerate((-1100.0, 0.0, 1100.0)):
        hull.box(f"post_{side}{n}", 80, 80, 580, at=(x, post_y, 1090), op="join")
        hull.box(f"link_{side}{n}", 90, 420, 140, at=(x, link_y, 830), op="join")

# Final-drive housings. The bore stops short of the bracket, so the cut stays in the housing.
# Left shaft occupies y 840 to 950. Right shaft, after the sprocket's half turn, y -950 to -840.
hull.cylinder("drive_l", 190, 140, at=(sx, 790, center_z), direction=(0, 1, 0), op="join")
hull.cylinder("bore_l", 46, 110, at=(sx, 830, center_z), direction=(0, 1, 0), op="cut")
hull.box("drive_neck_l", 220, 200, 220, at=(sx, 710, center_z), op="join")

hull.cylinder("drive_r", 190, 150, at=(sx, -940, center_z), direction=(0, 1, 0), op="join")
hull.cylinder("bore_r", 46, 125, at=(sx, -955, center_z), direction=(0, 1, 0), op="cut")
hull.box("drive_neck_r", 220, 200, 220, at=(sx, -710, center_z), op="join")

# Windows, cut after the shell is joined, then glazed.
hull.box("windshield_cut", 40, 1500, 820, at=(hull_front - 8, 0, 2620), op="cut")
hull.box("side_glass_cut", 1400, 2 * half_w + 80, 720, at=(1900, 0, 2680), op="cut")
hull.box("port_cut_l", 240, 60, 240, at=(-2500, half_w, 1950), op="cut")
hull.box("port_cut_r", 240, 60, 240, at=(-2500, -half_w, 1950), op="cut")

hull.box("windshield", 8, 1460, 780, at=(hull_front - 8, 0, 2620), op="new")
hull.box("glass_l", 1360, 8, 680, at=(1900, half_w - wall / 2.0, 2680), op="new")
hull.box("glass_r", 1360, 8, 680, at=(1900, -(half_w - wall / 2.0), 2680), op="new")
hull.box("port_l", 200, 8, 200, at=(-2500, half_w - wall / 2.0, 1950), op="new")
hull.box("port_r", 200, 8, 200, at=(-2500, -(half_w - wall / 2.0), 1950), op="new")

for i, x in enumerate((2000.0, 2320.0, 2640.0)):
    hull.cylinder(f"lamp_{i}", 34, 84, at=(x, 0, cab_roof), direction=(0, 0, 1), op="new")

# Pack case in the rear bay. The cells are a mass in the hand calculation, not a solid.
hull.box("pack", 1500, 900, 640, at=(-1600, 0, 1900), op="new")
hull.box("pack_void", 1472, 872, 612, at=(-1600, 0, 1906), op="cut", body="pack")

hull.material("aluminum-6061-t6", finish="painted", color="#1a1c1f")
hull.material("pc", bodies=["windshield", "glass_l", "glass_r", "port_l", "port_r"], color="#7eb6c9")
hull.appearance(opacity=0.4, roughness=0.05, bodies=["windshield", "glass_l", "glass_r", "port_l", "port_r"])
hull.material("pc", bodies=["lamp_0", "lamp_1", "lamp_2"], color="#f4f1e4")
