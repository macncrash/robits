from steve import Component
from params import base_h, shoulder_z
from shapes import cyl, ring

turret = Component("turret", name="Turret (J1 output, shoulder cradle)")
z_bottom = base_h + 100
body = cyl(65, (0, 0, (z_bottom + shoulder_z) / 2), "Z", shoulder_z - z_bottom)
body = body.cut(cyl(75, (0, 0, shoulder_z), "Y", 200))  # clears the J2 clamp lug (r 72.8) by 2 mm
turret.add("body", body, name="Cradle")
turret.add("accent", ring(69, 65, (0, 0, z_bottom + 5), "Z", 8), op="new", name="Blue ring")

turret.material("aluminum-6061-t6", finish="powder-coated", color="#23272e")
turret.material("aluminum-6061-t6", bodies=["accent"], finish="anodized", color="#2f6fd6")
