"""HSS tool bit 8 x 8 x 40, ground as a right-hand turning tool; cutting edge on centre (z 0) at the work's
radius. Sits on a 1 mm shim in the post's +Y pocket, back end against the post's centre column."""
import cadquery as cq
from steve import Component
from lathe_shapes import box
from lathe_params import carriage_x, tool_y

xc = carriage_x + 35
tip_y = -10.0                                                          # touching a 20 mm bar
bit = box(xc - 4, tool_y + 8, -8, xc + 4, tip_y - 6, 0)
nose = cq.Workplane("XY", origin=(0, 0, -8)).polyline([(xc - 4, tip_y - 6), (xc + 4, tip_y - 6), (xc + 1, tip_y),
                                                       (xc - 1, tip_y)]).close().extrude(8).val()
tool_bit = Component("tool_bit", name="HSS tool bit 8 x 8 x 40")
tool_bit.add("bit", bit.fuse(nose).clean(), name="Tool bit")
tool_bit.material("steel-1c60", finish="polished")
