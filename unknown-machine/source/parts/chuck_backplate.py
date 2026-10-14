"""Optional lathe attachment for the unknown-machine joint actuator: backplate for a bought 80 mm 3-jaw chuck.

Turns the actuator into a small lathe headstock. The plate bolts to the carrier front disk (the output) with
6 x ISO 4762 M4 x 12 in its six M4 load holes (PCD 50) and is located on the Ø20 output hub. A standard 80 mm
front-mount 3-jaw scroll chuck (DIN 6350 style: Ø55 rear recess, 3 x M6 from the front on PCD 66) sits on the
Ø55 spigot; its own three screws go into the M6 holes here. Check the bought chuck's recess and bolt circle
before machining: they vary a little between makers.
Coordinates are the actuator's (axis Z, output face at z 65.5); the plate sits from z 65.5 to the spigot face.
Material AISI 303 (1.4305); the library has no 303, so 304 stands in (same stiffness, slightly lower yield).
Parameters: spigot diameter and length, chuck bolt circle, plate thickness.
"""
import math

from steve import Model

spigot_d = 54.99  # mm Spigot into the chuck's Ø55 recess (55 h6: -0.010/-0.029 in production)
spigot_len = 2.5  # mm Spigot length (recess about 3 deep, so the chuck seats on the plate face)
chuck_pcd = 66  # mm Chuck mounting screw circle (3 x M6 from the chuck front)
plate_t = 12  # mm Plate thickness behind the chuck face
disk_face = 65.5  # mm Output disk front face (the plate's back)
relief_r = 34  # mm Back face relieved outside this radius (2 mm clear of the fixed front flange)

face = disk_face + plate_t  # chuck seats here

plate = Model("Lathe chuck backplate")
plate.cylinder("body", 40, plate_t, at=(0, 0, disk_face), name="Plate Ø80")
plate.cylinder("spigot", spigot_d / 2, spigot_len, at=(0, 0, face), op="join", name="Spigot Ø55 into the chuck")
plate.cylinder("relief", 40.5, 2, at=(0, 0, disk_face), op="cut", name="Back relief over the flange")
plate.cylinder("relief_keep", relief_r, 2, at=(0, 0, disk_face), op="join", name="Seat on the output disk")
plate.cylinder("pilot", 10, 6.8, at=(0, 0, disk_face), op="cut", name="Ø20 H7 pilot over the output hub")
plate.cylinder("bore", 8, plate_t + spigot_len, at=(0, 0, disk_face), op="cut", name="Ø16 through bore")
for k in range(6):                                   # 6 x M4 x 12 into the disk's load holes: head seat z 73,
    a = math.radians(60 * k + 30)                    # tip z 61 (0.5 mm in front of the disk's back face)
    x, y = 25 * math.cos(a), 25 * math.sin(a)
    plate.cylinder(f"m4_hole_{k + 1}", 2.25, plate_t + spigot_len, at=(x, y, disk_face), op="cut",
                   name=f"M4 clearance {k + 1}")
    plate.cylinder(f"m4_cbore_{k + 1}", 4.0, face + spigot_len - 73, at=(x, y, 73), op="cut",
                   name=f"M4 counterbore {k + 1}")
for k in range(3):                                   # chuck's 3 x M6: tapped (5.0 drill) 8 deep, between the M4s
    a = math.radians(120 * k)
    plate.cylinder(f"m6_{k + 1}", 2.5, 8, at=(chuck_pcd / 2 * math.cos(a), chuck_pcd / 2 * math.sin(a), face - 8),
                   op="cut", name=f"M6 tapped {k + 1}")
plate.material("stainless-304", finish="machined")   # specified AISI 303 (1.4305); 304 stand-in

result = plate.result()
