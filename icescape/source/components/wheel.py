"""Wheel. Antarctic: aluminium rim and a foam-filled urethane tire. Offworld: a metal hoop with radial cleats.

The tire is an annulus, not a solid puck, so its mass is a carcass rather than a rubber cylinder.
Urethane is not in the material library; polycarbonate is the density stand-in (about 1.2 g/cm³),
same as the band-saw tyres.
"""
import math

from steve import Component
from params import mission

wheel = Component("wheel", name="Wheel")

if mission == 0:
    # Hoop plus a thin web. A solid disk here was about 55 kg.
    wheel.cylinder("hoop", 250, 36, at=(0, -18, 0), direction=(0, 1, 0))
    wheel.cylinder("hoop_bore", 228, 46, at=(0, -23, 0), direction=(0, 1, 0), op="cut")
    wheel.cylinder("web", 228, 6, at=(0, -3, 0), direction=(0, 1, 0), op="join")
    wheel.cylinder("web_bore", 70, 16, at=(0, -8, 0), direction=(0, 1, 0), op="cut")
    wheel.cylinder("tire", 340, 150, at=(0, -75, 0), direction=(0, 1, 0), op="new")
    wheel.cylinder("tire_bore", 312, 160, at=(0, -80, 0), direction=(0, 1, 0), op="cut", body="tire")
    wheel.material("aluminum-6061-t6", finish="anodized", color="#1c2128")
    wheel.material("pc", bodies=["tire"], color="#14171c")
else:
    wheel.cylinder("hoop", 328, 140, at=(0, -70, 0), direction=(0, 1, 0))
    wheel.cylinder("hoop_bore", 292, 150, at=(0, -75, 0), direction=(0, 1, 0), op="cut")
    for i in range(12):
        a = math.radians(i * 30)
        s, c = math.sin(a), math.cos(a)
        wheel.cylinder(f"cleat_{i}", 9, 40, at=(300 * s, -70, 300 * c), direction=(s, 0, c), op="join")
    wheel.material("aluminum-6061-t6", finish="anodized", color="#c5d0d8")
