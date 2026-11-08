"""Side hatch. Origin is the forward edge, midway up, so the hinge is the Z axis.

The panel extends rearward, -X. Positive rotation about Z swings that edge toward -Y.
On the left side that is inward, so the left hatch opens on a negative angle.
"""
from steve import Component
from params import door_h, door_t, door_w

door = Component("door", name="Side hatch")

door.box("panel", door_w, door_t, door_h, at=(-door_w / 2.0, 0, 0))
door.box("window", 340, door_t + 12, 220, at=(-420, 0, 140), op="cut")
door.box("glass", 320, 8, 200, at=(-420, 0, 140), op="new")

door.material("aluminum-6061-t6", finish="painted", color="#1a1c1f")
door.material("pc", bodies=["glass"], color="#7eb6c9")
door.appearance(opacity=0.4, roughness=0.05, bodies=["glass"])
