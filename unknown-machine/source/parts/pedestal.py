"""Pedestal: saddle the housing bolts into, side cable port, square base plate with four holes.

The housing sits directly in the saddle (no clamp band) on a thermal pad, so the pedestal is also its heat sink.
It is held by four ISO 4762 M5 x 20 screws from below, in counterbores through the base, into tapped holes in
the housing, and located by two ISO 2338 4 m6 x 12 dowels. Coordinates are the actuator's: axis Z, pedestal -Y.
"""
import cadquery as cq
from steve import Model

saddle_r = 56.0  # mm Saddle radius under the housing's front section (housing Ø112)
fin_r = 48.0  # mm Saddle radius under the finned section (fin tips Ø96)
screw_x = 16  # mm Mount screws either side of the centre line
screw_z = (29, 39)  # mm Mount screw rows along the axis
dowel_z = (22, 40)  # mm Dowel positions on the centre line
head_y = -64  # mm Counterbore floor (screw head seat)

pedestal = Model("Pedestal")
pedestal.box("block", 80, 48, 64, at=(-40, -78, -20), centered=False, name="Saddle block")   # z -20..44: carries the finned section too
pedestal.cylinder("saddle", saddle_r, 33, at=(0, 0, 14), op="cut", name="Saddle")
pedestal.cylinder("saddle_fins", fin_r, 37, at=(0, 0, -23), op="cut", name="Saddle under the fins")
pedestal.box("cable_port", 82, 8, 14, at=(-41, -74, 10), centered=False, op="cut", name="Side cable port")
plate = cq.Workplane("XZ", origin=(0, -78, 0)).center(0, 22).rect(130, 100).extrude(10).edges("|Y").fillet(10).val()
pedestal.add("base_plate", plate, op="join", name="Base plate")
for k, (x, z) in enumerate(((-52, -15), (52, -15), (-52, 59), (52, 59))):   # 4 x M8 clearance (9 mm)
    pedestal.cylinder(f"bolt_hole_{k + 1}", 4.5, 12, at=(x, -77, z), direction=(0, -1, 0), op="cut",
                      name=f"Bolt hole {k + 1}")
for k, (x, z) in enumerate((x, z) for z in screw_z for x in (-screw_x, screw_x)):   # M5 x 20 from below
    pedestal.cylinder(f"screw_cbore_{k + 1}", 4.75, 25, at=(x, -89, z), direction=(0, 1, 0), op="cut",
                      name=f"Screw counterbore {k + 1}")
    pedestal.cylinder(f"screw_hole_{k + 1}", 2.75, 14, at=(x, head_y, z), direction=(0, 1, 0), op="cut",
                      name=f"Screw clearance {k + 1}")
for k, z in enumerate(dowel_z):                      # 4 mm dowel holes, 6 deep below the saddle
    pedestal.cylinder(f"dowel_hole_{k + 1}", 2, 7, at=(0, -62, z), direction=(0, 1, 0), op="cut",
                      name=f"Dowel hole {k + 1}")
pedestal.material("aluminum-6061-t6", finish="anodized", color="#1b2030")

result = pedestal.result()
