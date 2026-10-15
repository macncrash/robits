"""Planet carrier, front disk with the output hub (assembled position, z 60.5..72). Unknown-machine actuator.

Bolts to the rear part's three bridge posts with ISO 10642 M4 x 16 countersunk screws (11 mm of thread, 2.75 d) (heads flush with the
front face); the three ISO 2338 planet pins end in blind holes here and locate the two parts. The arm bolts to
the six M4 load holes. Bore the pin holes with both parts clamped together so the pins stay parallel.
Turned (disk, Ø20 g6 output pilot, relief groove at the pilot root) then drilled; pin holes bored with the rear
part clamped on. CNC notes: build-pack/cnc/carrier_disk.md.
Parameters: gear stage (sets the planet orbit), disk thickness, countersink diameter.
"""
import math

import cadquery as cq
from steve import Model

module = 1  # mm Gear module (pitch diameter = module x teeth)
sun_teeth = 18  # count Sun gear teeth
planet_teeth = 27  # count Planet gear teeth (ring = sun + 2 x planet)
disk_t = 5  # mm Front disk thickness (z 60.5 up)
csk_d = 9.0  # mm Countersink diameter for an ISO 10642 M4 head (90 deg, head 8.96): head flush, not sunk
pin_depth = 2  # mm Planet pin engagement in the disk

orbit = module * (sun_teeth + planet_teeth) / 2  # Planet centres
z0 = 60.5               # back face, against the posts
face = z0 + disk_t      # front face

disk = Model("Planet carrier front disk (output)")
disk.cylinder("disk", 33, disk_t, at=(0, 0, z0), name="Front disk")
disk.cylinder("hub", 10, 72 - face, at=(0, 0, face), op="join", name="Output hub")
disk.cylinder("cable_bore", 4, 72 - z0, at=(0, 0, z0), op="cut", name="Cable bore")
for k in range(3):                                   # blind holes for the planet pins (they end at z 62.5)
    a = math.radians(120 * k)
    disk.cylinder(f"pin_hole_{k + 1}", 3, pin_depth, at=(orbit * math.cos(a), orbit * math.sin(a), z0), op="cut",
                  name=f"Pin hole {k + 1}")
for k in range(3):                                   # M4 clearance holes + 90 deg countersinks over the posts
    a = math.radians(120 * k + 60)
    x, y = orbit * math.cos(a), orbit * math.sin(a)
    disk.cylinder(f"screw_hole_{k + 1}", 2.25, disk_t, at=(x, y, z0), op="cut", name=f"Screw clearance {k + 1}")
    h = (csk_d - 4.5) / 2
    cone = cq.Solid.makeCone(2.25, csk_d / 2, h, cq.Vector(x, y, face - h), cq.Vector(0, 0, 1))
    disk.add(f"csk_{k + 1}", cone, op="cut", name=f"Countersink {k + 1}")
for k in range(6):                                   # M4 tapped holes (tap drill 3.3) for the load, through the disk
    a = math.radians(60 * k + 30)
    disk.cylinder(f"load_hole_{k + 1}", 1.65, disk_t, at=(25 * math.cos(a), 25 * math.sin(a), z0), op="cut",
                  name=f"Load hole {k + 1}")
disk.add("pilot_relief", cq.Solid.makeCylinder(10.3, 1.1, cq.Vector(0, 0, face - 0.3)).cut(
    cq.Solid.makeCylinder(9.7, 1.1, cq.Vector(0, 0, face - 0.3))), op="cut", name="Relief 0.3 x 0.3 at the pilot root")


def edge_break(r, z, size, out, up):
    """45 deg chamfer ring at the circular edge (r, z) to cut away; out/up: the side the material is on."""
    e = 0.5
    pts = [(r + out * size, z), (r + out * size, z - up * e), (r - out * e, z - up * e), (r - out * e, z + up * size),
           (r, z + up * size)]
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0)).val()


for k, (r, z, size, out, up) in enumerate(((10, 72, 0.5, -1, -1),      # output pilot lead-in
                                           (4, 72, 0.3, 1, -1), (4, z0, 0.3, 1, 1),   # cable bore
                                           (33, face, 0.5, -1, -1), (33, z0, 0.3, -1, 1))):   # disk OD
    disk.add(f"edge_break_{k + 1}", edge_break(r, z, size, out, up), op="cut", name=f"Edge break {k + 1}")
disk.material("stainless-304", finish="brushed")   # specified AISI 303 (1.4305, free-machining); not in the library, 304 stand-in

result = disk.result()
