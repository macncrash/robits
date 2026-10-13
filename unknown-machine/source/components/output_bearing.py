"""Output bearing: crossed-roller CRBH 3510 (35 x 60 x 10) in the bulkhead. Carries the planet carrier and the
arm's radial, axial and tilting loads in one row (a single deep-groove 61806 could not take the moment)."""
import cadquery as cq
from steve import Component
from shapes import ring, turned

z0, width = 34, 10            # seat z 34..44
pitch_r, roller_d, n = 23.75, 3.5, 28

rollers = []
for k in range(n):            # rollers alternate +/-45 deg to the radius: the crossed arrangement
    roller = cq.Solid.makeCylinder(roller_d / 2, roller_d, cq.Vector(0, 0, -roller_d / 2), cq.Vector(0, 0, 1))
    roller = roller.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 45 if k % 2 == 0 else 135)
    rollers.append(turned(roller.translate(cq.Vector(pitch_r, 0, z0 + width / 2)), 360 * k / n))
rollers = cq.Compound.makeCompound(rollers)

output_bearing = Component("output_bearing", name="Output bearing CRBH 3510 (crossed roller)")
output_bearing.add("outer", ring(30, 24.5, width, z0).cut(rollers), name="Outer ring")
output_bearing.add("inner", ring(23, 17.5, width, z0).cut(rollers), op="new", name="Inner ring")
output_bearing.add("rollers", rollers, op="new", name="Rollers")
output_bearing.material("steel-1c60", finish="polished")
