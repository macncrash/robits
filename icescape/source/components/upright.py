"""Steering knuckle. The kingpin is under the steer actuator. The stub is the wheel axle.
The plate routes outboard of the drive actuator, which sits on the axle between the hub and the arm.
"""
from steve import Component

upright = Component("upright", name="Steering knuckle")

# Kingpin, up to the steer-actuator output face at z = 80.
upright.cylinder("kingpin", 16, 14, at=(0, -150, 66), direction=(0, 0, 1))
# Beam above the drive actuator, from the kingpin out to the side plate.
upright.box("beam", 96, 120, 12, at=(28, -145, 70), op="join")
# Side plate, outside the hub radius, down to axle height.
upright.box("plate", 26, 52, 76, at=(75, -104, 38), op="join")
# Dogleg into the axle, inboard of the tire.
upright.box("dogleg", 56, 12, 28, at=(44, -72, 0), op="join")
# Stub axle. The hub pilot ends at y = -78; this starts there.
upright.cylinder("stub", 20, 32, at=(0, -78, 0), direction=(0, 1, 0), op="join")

upright.material("aluminum-6061-t6", finish="anodized", color="#343b44")
