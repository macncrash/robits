"""Tool rests (two, mirror images): a 33 x 50 steel table at the wheel's centre height, 2 mm off the wheel, on an
arm bolted through a slot to the guard's inner wall so it can follow the wheel as it wears."""
from steve import Component
from grinder_shapes import box
from grinder_params import spindle_z, wheel_d, rest_gap

H = spindle_z
edge = -(wheel_d / 2 + rest_gap)


def rest():
    table = box(101, edge - 33, H - 6, 150, edge, H)
    arm = box(101, -95, H - 60, 105, -60, H - 6)
    return table.fuse(arm).clean()


right = rest()
tool_rests = Component("tool_rests", name="Tool rests")
tool_rests.add("rest_right", right, name="Tool rest, right")
tool_rests.add("rest_left", right.mirror("YZ"), op="new", name="Tool rest, left")
tool_rests.material("steel-s235jr", color="#1d1f22")
