"""Wheel covers (2 mm steel, powder coated): a box over the front of each wheel, closed to the frame plates
behind, with a door knob each (the doors hinge on the left in practice; drawn closed). The upper cover's floor
has a slot for the blade; the lower cover's top is the frame's shelf. A stiff brush inside the lower cover
sweeps chips off the blade where it leaves the cut."""
from steve import Component
from bandsaw_shapes import box, ycyl, one


def cover(z0, z1):
    front = box(-33, -35, z0, 280, -32, z1)
    left = box(-33, -35, z0, -30, 30, z1)
    top = box(-33, -35, z1 - 3, 280, 30, z1)
    bottom = box(-33, -35, z0, 238, 30, z0 + 3).cut(box(-10, -16, z0 - 1, 10, 16, z0 + 4))   # blade slot
    knob = ycyl(8, -45, -35, 230, (z0 + z1) / 2)
    return front.fuse(left).fuse(top).fuse(bottom).fuse(knob)


upper = cover(140, 412)
lower = box(-33, -35, -392, 280, -32, -100).fuse(box(-33, -35, -392, -30, 30, -100))
lower = lower.fuse(box(-33, -35, -392, 280, 30, -389)).fuse(ycyl(8, -45, -35, 230, -246))
brush = box(-22, -8, -160, -1.0, 8, -145).fuse(box(-30, -4, -156, -22, 4, -149))
wheel_covers = Component("wheel_covers", name="Wheel covers and chip brush")
wheel_covers.add("covers", one(upper.clean(), lower.clean(), brush.clean()), name="Wheel covers and chip brush")
wheel_covers.material("steel-s235jr", color="#7a2a22")           # machine red, powder coated
