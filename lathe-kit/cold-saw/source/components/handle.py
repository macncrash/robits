"""Handle with trigger switch, bolted to the gearbox's top face: pull down to cut, the trigger runs the drive (a
dead-man switch; the drive's ramp stops the blade in about a second when it is let go)."""
from steve import Component
from coldsaw_shapes import box, zcyl, xcyl
from coldsaw_params import gear_x

h = zcyl(10, 250, 310, gear_x, -70).fuse(box(gear_x - 10, -130, 300, gear_x + 10, -60, 320))
h = h.fuse(xcyl(14, 14, 134, -120, 310))
trigger = box(gear_x - 4, -126, 284, gear_x + 4, -116, 296.5)
handle = Component("handle", name="Handle and trigger")
handle.add("handle", h.clean(), name="Handle")
handle.add("trigger", trigger, name="Trigger")
handle.material("steel-s235jr", color="#2a2c30")
handle.material("steel-s235jr", bodies=["trigger"], color="#b8401f")
