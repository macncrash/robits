"""Planet carrier = output: rear plate with a sleeve in the output bearing, three pins, front disk and hub."""
import math

from steve import Model
# Parameters (from the design's params.py when this was extracted)
module = 1  # mm Gear module (pitch diameter = module x teeth)
sun_teeth = 18  # count Sun gear teeth
planet_teeth = 27  # count Planet gear teeth (ring = sun + 2 x planet)

orbit = module * (sun_teeth + planet_teeth) / 2  # Planet centres

post_r = 6  # mm Bridge posts between the planets (2 mm clear of the planet tip circles)

carrier = Model("Planet carrier (output)")
carrier.cylinder("sleeve", 15, 10.5, at=(0, 0, 37), name="Sleeve")                 # in the 61806, z 37..47.5
carrier.cylinder("plate", 33, 3, at=(0, 0, 44.5), op="join", name="Rear plate")
for k in range(3):                                                                  # posts tie the plates together
    a = math.radians(120 * k + 60)
    carrier.cylinder(f"post_{k + 1}", post_r, 13, at=(orbit * math.cos(a), orbit * math.sin(a), 47.5), op="join",
                     name=f"Bridge post {k + 1}")
carrier.cylinder("disk", 33, 3, at=(0, 0, 60.5), op="join", name="Front disk")
carrier.cylinder("hub", 10, 8.5, at=(0, 0, 63.5), op="join", name="Output hub")
carrier.cylinder("needle_seat", 9, 10.5, at=(0, 0, 37), op="cut", name="Needle bearing seat")
carrier.cylinder("cable_bore", 4, 30, at=(0, 0, 47.5), op="cut", name="Cable bore")
for k in range(3):                                   # ISO 2338 6x18 planet pins: flush with the rear plate, blind to z 62.5
    a = math.radians(120 * k)
    carrier.cylinder(f"pin_hole_{k + 1}", 3, 18, at=(orbit * math.cos(a), orbit * math.sin(a), 44.5), op="cut",
                     name=f"Pin hole {k + 1}")
for k in range(6):                                   # M4 tapped holes (tap drill 3.3) for the load
    a = math.radians(60 * k + 30)
    carrier.cylinder(f"load_hole_{k + 1}", 1.65, 3, at=(25 * math.cos(a), 25 * math.sin(a), 61), op="cut",
                     name=f"Load hole {k + 1}")
carrier.material("stainless-304", finish="brushed")

result = carrier.result()
