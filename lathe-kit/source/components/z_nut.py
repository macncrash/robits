"""Z ball nut (branch "milling"): SFU1204 flanged nut in the Z slide's block, flange on top (4 x M4)."""
import cadquery as cq
from steve import Component
from lathe_shapes import ball_nut
from lathe_params import mill_spindle_y

z_nut = Component("z_nut", name="Z ball nut SFU1204 (bought)")
z_nut.add("nut", ball_nut().translate(cq.Vector(79, mill_spindle_y, 140)), name="Ball nut")
z_nut.material("steel-1c60", finish="machined", color="#4a4d52")
