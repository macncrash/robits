from steve import Component
from params import w2_x, w_y, a6_z
from shapes import cyl, box

tool = Component("tool", name="Gripper body (J6 output)")
z_flange = a6_z - 42.5  # J6 output face
tool.add("accent", cyl(40, (w2_x, w_y, z_flange - 5), "Z", 10), name="Tool flange")
tool.add("body", box(110, 64, 50, (w2_x, w_y, z_flange - 35), fillet_z=10), op="new", name="Gripper housing")
tool.add("rail", box(120, 22, 8, (w2_x, w_y, z_flange - 64)), op="new", name="Finger rail")

tool.material("aluminum-7075-t6", finish="anodized", color="#1d2027")
tool.material("aluminum-6061-t6", bodies=["accent"], finish="anodized", color="#2f6fd6")
tool.material("stainless-304", bodies=["rail"], finish="machined")
