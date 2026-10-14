"""Sample work: 20 mm bar in the chuck, supported by the live centre in a 60-degree centre hole."""
import cadquery as cq
from steve import Component
from lathe_shapes import xcyl

tip = 258.14 - 0.05                                   # centre hole apex, 0.05 short of the live-centre point
bar = xcyl(10, 129, 262)
bar = bar.cut(cq.Solid.makeCone(0.01, (262 - tip) * 0.57735, 262 - tip, cq.Vector(tip, 0, 0), cq.Vector(1, 0, 0)))
workpiece = Component("workpiece", name="Work: 20 mm bar")
workpiece.add("bar", bar.clean(), name="Bar")
workpiece.material("aluminum-6061-t6", finish="machined")
