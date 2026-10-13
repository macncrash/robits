"""Planet carrier, rear part: sleeve in the CRBH 3510 output bearing, rear plate and three bridge posts.

The carrier is made in two pieces so it can be machined from the open front face: this rear part (posts milled
from the front) and a bolted front disk with the output hub (separate part). Three ISO 10642 M4 x 12 countersunk
screws go through the disk into the posts; the three ISO 2338 planet pins pass through both and locate them.
Parameters: gear stage (sets the planet orbit), post radius, screw tapping depth.
"""
import math

from steve import Model

module = 1  # mm Gear module (pitch diameter = module x teeth)
sun_teeth = 18  # count Sun gear teeth
planet_teeth = 27  # count Planet gear teeth (ring = sun + 2 x planet)
post_r = 6  # mm Bridge posts between the planets (2 mm clear of the planet tip circles)
tap_depth = 9  # mm M4 tapped hole depth in each post (screw engages 7 mm)

orbit = module * (sun_teeth + planet_teeth) / 2  # Planet centres

carrier = Model("Planet carrier rear (output)")
carrier.cylinder("sleeve", 17.5, 13.5, at=(0, 0, 34), name="Sleeve")               # in the CRBH 3510 crossed-roller bearing, z 34..47.5
carrier.cylinder("plate", 33, 3, at=(0, 0, 44.5), op="join", name="Rear plate")
for k in range(3):                                                                  # posts, z 47.5..60.5, meet the front disk
    a = math.radians(120 * k + 60)
    carrier.cylinder(f"post_{k + 1}", post_r, 13, at=(orbit * math.cos(a), orbit * math.sin(a), 47.5), op="join",
                     name=f"Bridge post {k + 1}")
carrier.cylinder("needle_seat", 9, 10.5, at=(0, 0, 37), op="cut", name="Needle bearing seat")
carrier.cylinder("shaft_clearance", 7, 3, at=(0, 0, 34), op="cut", name="Shaft clearance")   # motor shaft (12 mm) passes behind the needle seat
for k in range(3):                                   # ISO 2338 6x18 planet pins, pressed through the rear plate
    a = math.radians(120 * k)
    carrier.cylinder(f"pin_hole_{k + 1}", 3, 3, at=(orbit * math.cos(a), orbit * math.sin(a), 44.5), op="cut",
                     name=f"Pin hole {k + 1}")
for k in range(3):                                   # M4 tapped holes (tap drill 3.3) for the front-disk screws
    a = math.radians(120 * k + 60)
    carrier.cylinder(f"screw_hole_{k + 1}", 1.65, tap_depth, at=(orbit * math.cos(a), orbit * math.sin(a), 60.5 - tap_depth),
                     op="cut", name=f"M4 tapped hole {k + 1}")
carrier.material("stainless-304", finish="brushed")   # specified AISI 303 (1.4305, free-machining); not in the library, 304 stand-in

result = carrier.result()
