"""Planet carrier, rear part: sleeve in the CRBH 3510 output bearing, rear plate and three bridge posts.

The carrier is made in two pieces so it can be machined from the open front face: this rear part (posts milled
from the front) and a bolted front disk with the output hub (separate part). Three ISO 10642 M4 x 16 countersunk
screws go through the disk into the posts (11 mm of thread, 2.75 d); the three ISO 2338 planet pins pass through both and locate them.
Machined from 303 bar: turn the sleeve, needle seat and plate, then mill the posts from the front (3-axis, a
Ø6 R1 bull-nose leaves the 1 mm post-root fillet). The CRBH 3510 inner ring (z 32.5..42.5) banks against a Ø41
shoulder and is held by a DIN 471 35 x 1.5 ring in a groove behind it; the HK1210 (12 x 16 x 10) presses into a
Ø16 seat. CNC notes: build-pack/cnc/carrier.md.
Parameters: gear stage (sets the planet orbit), post radius, screw tapping depth.
"""
import math

import cadquery as cq
from steve import Model

module = 1  # mm Gear module (pitch diameter = module x teeth)
sun_teeth = 18  # count Sun gear teeth
planet_teeth = 27  # count Planet gear teeth (ring = sun + 2 x planet)
post_r = 6  # mm Bridge posts between the planets (2 mm clear of the planet tip circles)
tap_depth = 13  # mm M4 tap-drill depth in each post (Ø3.3 + 118 deg point; full thread 11.5, the M4 x 16 engages 11)
post_fillet = 1.0  # mm Fillet at the post roots (bull-nose cutter radius)
sleeve_fillet = 0.4  # mm Fillet at the shoulder-to-plate corner

orbit = module * (sun_teeth + planet_teeth) / 2  # Planet centres

carrier = Model("Planet carrier rear (output)")
carrier.cylinder("sleeve", 17.5, 16.6, at=(0, 0, 27.9), name="Sleeve")             # in the CRBH 3510 crossed-roller bearing (z 32.5..42.5)
carrier.cylinder("shoulder", 20.5, 2, at=(0, 0, 42.5), op="join", name="Bearing shoulder")   # z 42.5..44.5, inner ring banks on it
carrier.cylinder("plate", 33, 3, at=(0, 0, 44.5), op="join", name="Rear plate")
for k in range(3):                                                                  # posts, z 47.5..60.5, meet the front disk
    a = math.radians(120 * k + 60)
    carrier.cylinder(f"post_{k + 1}", post_r, 13, at=(orbit * math.cos(a), orbit * math.sin(a), 47.5), op="join",
                     name=f"Bridge post {k + 1}")
carrier.cylinder("needle_seat", 8, 10.5, at=(0, 0, 37), op="cut", name="Needle bearing seat")   # HK1210 drawn cup, Ø16 N6
carrier.cylinder("shaft_clearance", 7, 9.1, at=(0, 0, 27.9), op="cut", name="Shaft clearance")   # motor shaft (12 mm) passes behind the needle seat
for k in range(3):                                   # ISO 2338 6x18 planet pins, pressed through the rear plate
    a = math.radians(120 * k)
    carrier.cylinder(f"pin_hole_{k + 1}", 3, 3, at=(orbit * math.cos(a), orbit * math.sin(a), 44.5), op="cut",
                     name=f"Pin hole {k + 1}")
for k in range(3):                                   # M4 tapped holes (tap drill 3.3) for the front-disk screws
    a = math.radians(120 * k + 60)
    carrier.cylinder(f"screw_hole_{k + 1}", 1.65, tap_depth, at=(orbit * math.cos(a), orbit * math.sin(a), 60.5 - tap_depth),
                     op="cut", name=f"M4 tapped hole {k + 1}")
carrier.fillet("post_roots", edges=[f"edge(post_{k + 1}.side|plate.top)" for k in range(3)], radius=post_fillet,
               name="Post root fillets")
carrier.fillet("sleeve_root", edges=["edge(shoulder.side|plate.bottom)"], radius=sleeve_fillet, name="Shoulder-to-plate fillet")
carrier.add("circlip_groove", cq.Solid.makeCylinder(18, 1.6, cq.Vector(0, 0, 30.9)).cut(
    cq.Solid.makeCylinder(16.5, 1.6, cq.Vector(0, 0, 30.9))), op="cut", name="DIN 471 35 groove (Ø33 x 1.6)")
carrier.add("shoulder_relief", cq.Solid.makeCylinder(17.8, 1.1, cq.Vector(0, 0, 41.7)).cut(
    cq.Solid.makeCylinder(17.2, 1.1, cq.Vector(0, 0, 41.7))), op="cut", name="Relief 0.3 x 0.3 at the shoulder")
for k in range(3):                                   # 118 deg drill points under the tapped holes
    a = math.radians(120 * k + 60)
    tip = cq.Solid.makeCone(1.65, 0, 1.65 / math.tan(math.radians(59)),
                            cq.Vector(orbit * math.cos(a), orbit * math.sin(a), 60.5 - tap_depth), cq.Vector(0, 0, -1))
    carrier.add(f"drill_point_{k + 1}", tip, op="cut", name=f"Drill point {k + 1}")


def edge_break(r, z, size, out, up):
    """45 deg chamfer ring at the circular edge (r, z) to cut away; out/up: the side the material is on."""
    e = 0.5
    pts = [(r + out * size, z), (r + out * size, z - up * e), (r - out * e, z - up * e), (r - out * e, z + up * size),
           (r, z + up * size)]
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0)).val()


for k, (r, z, size, out, up) in enumerate(((17.5, 27.9, 0.5, -1, 1),   # lead-in for the CRBH inner ring
                                           (8, 47.5, 0.5, 1, -1),    # lead-in for pressing the HK1210 cup
                                           (7, 27.9, 0.3, 1, 1), (20.5, 42.5, 0.3, -1, 1),
                                           (33, 44.5, 0.3, -1, 1), (33, 47.5, 0.3, -1, -1))):   # plate OD
    carrier.add(f"edge_break_{k + 1}", edge_break(r, z, size, out, up), op="cut", name=f"Edge break {k + 1}")
carrier.material("stainless-304", finish="brushed")   # specified AISI 303 (1.4305, free-machining); not in the library, 304 stand-in

result = carrier.result()
