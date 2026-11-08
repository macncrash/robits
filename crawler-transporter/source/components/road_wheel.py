"""Road wheel. It rolls on the inner face of the bottom shoe, with a gap.

The arm that carries it is on the hull, fixed at ride height. The shoe band
does not deflect, so the wheel cannot travel.
"""
from steve import Component
from params import wheel_r, wheel_w

road_wheel = Component("road_wheel", name="Road wheel")

road_wheel.cylinder("rim", wheel_r, wheel_w, at=(0, -wheel_w / 2.0, 0), direction=(0, 1, 0))
road_wheel.cylinder("pocket", wheel_r - 40, wheel_w - 56, at=(0, -wheel_w / 2.0 + 28, 0), direction=(0, 1, 0), op="cut")
road_wheel.cylinder("bore", 40, wheel_w + 8, at=(0, -wheel_w / 2.0 - 4, 0), direction=(0, 1, 0), op="cut")

road_wheel.material("steel-a36", finish="painted", color="#3a3f46")
