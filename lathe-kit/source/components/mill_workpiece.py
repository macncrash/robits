"""Workpiece for the milling pose (branch "milling"): 6061 block 40 x 30 x 38 in the vise, with a 6.2-wide,
3-deep slot cut from its left end up to the cutter."""
from steve import Component
from lathe_shapes import box, zcyl
from lathe_params import carriage_x, mill_spindle_x, mill_spindle_y

xc = carriage_x + 35
block = box(xc - 20, -60, -44, xc + 20, -30, -6)
slot = box(xc - 21, mill_spindle_y - 3.1, -9.1, mill_spindle_x, mill_spindle_y + 3.1, -5)
slot = slot.fuse(zcyl(3.1, -9.1, -5, mill_spindle_x, mill_spindle_y))
mill_workpiece = Component("mill_workpiece", name="Workpiece (6061 block)")
mill_workpiece.add("block", block.cut(slot).clean(), name="Workpiece")
mill_workpiece.material("aluminum-6061-t6", finish="machined")
