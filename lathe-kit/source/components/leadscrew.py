"""Carriage leadscrew: SFU1204 ball screw (Ø12, 4 mm lead, rolled C7, ends machined to Ø10) along the front of
the bed, turned by the handwheel at the right end; 4 mm of carriage travel per turn, 0.02 mm per line on the
200-line dial. Grooved from x -24 to 436; Ø10 journals in the two brackets (bronze bush on the left, two
AXK1024 thrust washers either side of the right bracket to take the end load)."""
import cadquery as cq
from steve import Component
from lathe_shapes import ball_screw

leadscrew = Component("leadscrew", name="Leadscrew SFU1204 ball screw")
screw = ball_screw(-24, 436, journals=((-35, -24), (436, 470)))
screw = screw.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), 90).translate(cq.Vector(0, -67.5, -120))
leadscrew.add("screw", screw, name="Leadscrew")
leadscrew.material("steel-1c60", finish="machined")
