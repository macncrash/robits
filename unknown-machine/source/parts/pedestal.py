"""Pedestal: saddle that cradles the clamp band, side cable port, square base plate with four holes."""
import cadquery as cq
from steve import Model

saddle_r = 60.2  # mm Saddle radius (clamp band OD 120 + clearance)

pedestal = Model("Pedestal")
pedestal.box("block", 80, 48, 44, at=(-40, -78, 0), centered=False, name="Saddle block")
pedestal.cylinder("saddle", saddle_r, 50, at=(0, 0, -3), op="cut", name="Saddle")
pedestal.box("cable_port", 82, 8, 14, at=(-41, -74, 10), centered=False, op="cut", name="Side cable port")
plate = cq.Workplane("XZ", origin=(0, -78, 0)).center(0, 22).rect(130, 100).extrude(10).edges("|Y").fillet(10).val()
pedestal.add("base_plate", plate, op="join", name="Base plate")
for k, (x, z) in enumerate(((-52, -15), (52, -15), (-52, 59), (52, 59))):   # 4 x M8 clearance (9 mm)
    pedestal.cylinder(f"bolt_hole_{k + 1}", 4.5, 12, at=(x, -77, z), direction=(0, -1, 0), op="cut",
                      name=f"Bolt hole {k + 1}")
pedestal.material("aluminum-6061-t6", finish="anodized", color="#1b2030")

result = pedestal.result()
