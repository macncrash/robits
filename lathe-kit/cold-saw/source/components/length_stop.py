"""Length stop: Ø16 rod from the base's bracket out to the right, and a sliding stop finger with a lock screw;
set to the length on the fence rule for repeat cuts."""
from steve import Component
from coldsaw_shapes import box, xcyl

rod = xcyl(8, 245, 390, 40, 62)
finger = box(300, 28, 50, 316, 52, 74).cut(xcyl(8.05, 299, 317, 40, 62))
finger = finger.fuse(box(300, -40, 40, 303, 28, 66))
length_stop = Component("length_stop", name="Length stop")
length_stop.add("rod", rod, name="Rod")
length_stop.add("finger", finger.clean(), name="Stop finger")
length_stop.material("steel-1c45", finish="polished")
