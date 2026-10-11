"""Planet carrier = output: rear plate with a sleeve in the output bearing, three pins, front disk and hub."""
import math

import cadquery as cq
from steve import Component
from params import module, sun_teeth, planet_teeth
from shapes import cyl, ring

orbit = module * (sun_teeth + planet_teeth) / 2  # Planet centres

carrier = Component("carrier", name="Planet carrier (output)")
body = ring(15, 9, 10.5, 37).fuse(ring(33, 9, 3, 44.5))            # sleeve z 37..47.5, rear plate
for k in range(3):
    a = math.radians(120 * k)
    body = body.fuse(cyl(3, 13, 47.5, orbit * math.cos(a), orbit * math.sin(a)))   # pins
body = body.fuse(cyl(33, 3, 60.5)).fuse(cyl(10, 8.5, 63.5))       # front disk, output hub
body = body.cut(cyl(4, 40, 55))                                     # hollow output (cable bore)
for k in range(6):                                                  # tapped holes for the load
    a = math.radians(60 * k + 30)
    body = body.cut(cyl(1.6, 3, 61, 25 * math.cos(a), 25 * math.sin(a)))
carrier.add("body", body.clean(), name="Carrier")
carrier.material("stainless-304", finish="brushed")
