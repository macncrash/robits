"""Rear drive sprocket. The disk is the envelope. Ten lugs stand in for the teeth.

Tooth tips stay 10 mm inside the shoe. They do not mesh: the band is a ring,
not a pitched chain. The shaft reaches inboard into the final-drive bore.
"""
import math

from steve import Component
from params import sprocket_r, tooth_tip

sprocket = Component("sprocket", name="Drive sprocket")

sprocket.cylinder("disk", sprocket_r, 140, at=(0, -70, 0), direction=(0, 1, 0))
sprocket.cylinder("pocket_a", 450, 48, at=(0, -68, 0), direction=(0, 1, 0), op="cut")
sprocket.cylinder("pocket_b", 450, 48, at=(0, 18, 0), direction=(0, 1, 0), op="cut")
sprocket.cylinder("shaft_in", 32, 110, at=(0, -180, 0), direction=(0, 1, 0), op="join")
sprocket.cylinder("shaft_out", 32, 100, at=(0, 70, 0), direction=(0, 1, 0), op="join")

tooth_h = tooth_tip - 500.0
for i in range(10):
    a = 2.0 * math.pi * i / 10.0
    c, s = math.cos(a), math.sin(a)
    sprocket.cylinder(
        f"tooth_{i}",
        22,
        tooth_h,
        at=(500.0 * c, -16, 500.0 * s),
        direction=(c, 0, s),
        op="join",
    )

sprocket.material("steel-34crnimo6", finish="machined", color="#3c4148")
