"""Ø6 HSS-Co end mill, 2 flutes, 57 long (bought), in the ER20 collet: shank z 85..122, flutes to the tip at
z 142 in the actuator's frame (cutter tip at z -9 in the mill pose, in the slot it has cut)."""
import cadquery as cq
from steve import Component

shank = cq.Solid.makeCylinder(3, 37, cq.Vector(0, 0, 85), cq.Vector(0, 0, 1))
flutes = cq.Solid.makeCylinder(3, 20, cq.Vector(0, 0, 122), cq.Vector(0, 0, 1))
for a in (0, 180):
    gash = cq.Solid.makeBox(4, 2.4, 20, cq.Vector(0.6, -1.2, 122)).rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a + 20)
    flutes = flutes.cut(gash)
end_mill = Component("end_mill", name="End mill Ø6 HSS-Co (bought)")
end_mill.add("shank", shank, name="Shank")
end_mill.add("flutes", flutes, name="Flutes")
end_mill.material("steel-1c60", finish="polished", color="#9aa0a8")
