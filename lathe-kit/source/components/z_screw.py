"""Z screw (branch "milling"): SFU1204 ball screw, vertical in the column channel, grooved z -60..220, Ø10
journal through the cap into the handwheel. Fixed axially at the cap; the free lower end needs no bearing at hand
speeds. A ball screw back-drives under the head's weight (about 60 N, 0.04 N m on the wheel), so the cap has a
spring-loaded brass drag plug on the journal and the slide a lock lever: set the drag so the head stays put."""
import cadquery as cq
from steve import Component
from lathe_shapes import ball_screw
from lathe_params import mill_spindle_y

z_screw = Component("z_screw", name="Z screw SFU1204 ball screw")
screw = ball_screw(-60, 220, journals=((220, 266),))
z_screw.add("screw", screw.translate(cq.Vector(79, mill_spindle_y, 0)), name="Z screw")
z_screw.material("steel-1c60", finish="machined")
