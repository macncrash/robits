"""Deep-groove ball bearing 6204-2RS (bought): 20 x 47 x 14, sealed. Modelled on the right (x 46..60)."""
from steve import Component
from grinder_shapes import xring

bearing_6204 = Component("bearing_6204", name="Bearing 6204-2RS")
bearing_6204.add("bearing", xring(23.5, 10, 46, 60), name="6204-2RS")
bearing_6204.material("steel-1c60", finish="polished")
