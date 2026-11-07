"""Wedge hull. Belly at z = 280 mm. The cavity is closed: battery bay and GPR skid sit in it
as their own bodies. Clevis ears bracket each swing arm with a gap, so the arm can move;
the pin itself is the revolute joint, not a modelled pin.
"""
from steve import Component
from params import half_wb, half_track, wheel_r, arm_y0, arm_z, arm_h

hull = Component("hull", name="Hull")

with hull.sketch("profile", on="XZ") as s:
    s.polyline("side", [
        (-1020, 280),
        (780, 280),
        (1280, 460),
        (860, 700),
        (420, 780),
        (-80, 780),
        (-520, 640),
        (-1020, 560),
    ])
# both=True splits distance across the two directions, so 560 mm is ±280.
hull.extrude("skin", "profile", distance=560, both=True)

# About 12 mm inside the outer profile, including the nose, so the wedge is a shell.
# Cavity width is ±272, an 8 mm side wall.
with hull.sketch("inner", on="XZ") as s:
    s.polyline("void", [
        (-1008.0, 292.0),
        (777.9, 292.0),
        (1251.5, 462.5),
        (855.8, 688.6),
        (418.9, 768.0),
        (-78.1, 768.0),
        (-517.2, 628.3),
        (-1008.0, 549.8),
    ])
hull.extrude("cavity", "inner", distance=544, both=True, op="cut")

# Clevis ears, joined while the skin is the only body. Two per corner, above and below
# the arm, 9 mm clear of it at ride height. The pin itself is the revolute.
arm_top = wheel_r + arm_z + arm_h / 2
arm_bot = wheel_r + arm_z - arm_h / 2
for end, x in (("f", half_wb), ("r", -half_wb)):
    for side, sign in (("l", 1), ("r", -1)):
        y_face = sign * (half_track + arm_y0)
        for k, zc in (("lo", arm_bot - 16), ("hi", arm_top + 16)):
            hull.box(
                f"ear_{end}{side}{k}",
                70,
                80,
                14,
                at=(x, y_face, zc),
                op="join",
            )

# Battery case, a shell. The cells are a mass in the hand calculation, not a solid here.
hull.box("pack", 620, 300, 160, at=(-180, 0, 470), op="new")
hull.box("pack_void", 604, 284, 144, at=(-180, 0, 474), op="cut", body="pack")

# Nose skid, also the GPR antenna bay cover. It hangs 8 mm below the belly.
hull.box("skid", 360, 280, 8, at=(560, 0, 276), op="new")

# Canopy, a window, not a pressure cabin. Internal height is not a seat.
hull.box("glass", 460, 340, 12, at=(170, 0, 786), op="new")

# Rear deck, 6 mm plate, 2 mm off the tail slope. Antarctic solar cover; offworld, the radiator face.
# Tail from (-1020, 560) to (-520, 640). Outward normal is (-80, 500) / length.
with hull.sketch("deck_profile", on="XZ") as s:
    s.polyline("deck_loop", [
        (-980.3, 568.4),
        (-760.3, 603.6),
        (-761.3, 609.5),
        (-981.3, 574.3),
    ])
hull.extrude("deck", "deck_profile", distance=300, both=True, op="new")

# Light bar, 10 mm plate, 2 mm off the windshield slope, ahead of the canopy.
# Slope from (420, 780) to (860, 700). Outward normal is (80, 440) / length.
with hull.sketch("lamp_profile", on="XZ") as s:
    s.polyline("lamp_loop", [
        (640.4, 742.0),
        (840.4, 705.6),
        (842.1, 715.4),
        (642.1, 751.8),
    ])
hull.extrude("lamp", "lamp_profile", distance=320, both=True, op="new")

# Rear tab: the antenna mast.
hull.cylinder("mast", 8, 260, at=(-1000, 0, 560), direction=(0, 0, 1), op="new")

hull.material("aluminum-6061-t6", finish="anodized", color="#2c333b")
hull.material("aluminum-6061-t6", bodies=["pack"], finish="anodized", color="#1a1e24")
hull.material("aluminum-6061-t6", bodies=["skid"], finish="anodized", color="#3d4a55")
hull.material("pc", bodies=["glass"], color="#c5e6f0")
hull.material("aluminum-6061-t6", bodies=["deck"], finish="anodized", color="#1b2838")
hull.material("aluminum-6061-t6", bodies=["lamp"], finish="anodized", color="#d7f4ff")
hull.material("stainless-304", bodies=["mast"], finish="brushed")
hull.appearance(opacity=0.35, bodies=["glass"])
