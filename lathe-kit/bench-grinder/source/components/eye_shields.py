"""Eye shields (two): 3 mm polycarbonate, 50 x 65, clamped on the guard arms in front of the wheels. Wear safety
glasses as well."""
from steve import Component
from grinder_shapes import box
from grinder_params import spindle_z

shield = box(105, -95, spindle_z + 40, 155, -92, spindle_z + 105)
eye_shields = Component("eye_shields", name="Eye shields (polycarbonate)")
eye_shields.add("shield_right", shield, name="Eye shield, right")
eye_shields.add("shield_left", shield.mirror("YZ"), op="new", name="Eye shield, left")
eye_shields.material("pc", color="#9fb4c8")
