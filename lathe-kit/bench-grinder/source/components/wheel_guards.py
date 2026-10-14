"""Wheel guards (cast aluminium, two, mirror images): neck flange on the end bell (3 x M5), a closed shroud round
each wheel, opened only from 10 degrees below the horizontal to 65 degrees above it on the operator's side. Each
carries a steel spark deflector (tongue guard) 3 mm off the wheel, slotted to follow the wheel down as it wears,
and the arm for the eye shield."""
import math
from steve import Component
from grinder_shapes import xcyl, xring, ycyl, box, wedge, sector
from grinder_params import spindle_z, wheel_d, guard_open

H = spindle_z
r_band = wheel_d / 2 + 10                      # shroud inside radius: 10 mm round the new wheel
x0, x1 = 105, 156                              # inner wall face .. outer cover face


def guard():
    neck = xring(40, 17, 62, 68)
    for a in (90, 210, 330):
        y, z = 34 * math.cos(math.radians(a)), H + 34 * math.sin(math.radians(a))
        neck = neck.cut(xcyl(2.75, 61, 69, y, z))
    neck = neck.fuse(xring(26, 17, 68, x0))
    shell = xcyl(r_band + 4, x0, x1).cut(xcyl(r_band, x0 + 4, x1 - 4)).cut(xcyl(17, x0 - 1, x0 + 5))
    shell = shell.cut(wedge(-10, guard_open, x0 - 1, x1 + 1).cut(xcyl(50, x0 - 2, x1 + 2)))
    post = box(126, -5, H + r_band + 3, 134, 5, H + r_band + 17)
    rod = ycyl(4, -88, -4, 130, H + r_band + 12)
    clamp = box(124, -92, H + r_band + 7, 136, -84, H + r_band + 17)
    return neck.fuse(shell).fuse(post).fuse(rod).fuse(clamp).clean()


def deflector():
    strip = sector(r_band + 6, r_band + 4, guard_open - 1, 85, x0, x1)
    lip = sector(r_band + 6, wheel_d / 2 + 3, guard_open - 2.5, guard_open - 0.5, x0, x1)
    return strip.fuse(lip).clean()


right, spark = guard(), deflector()
wheel_guards = Component("wheel_guards", name="Wheel guards with spark deflectors")
wheel_guards.add("guard_right", right, name="Guard, right")
wheel_guards.add("guard_left", right.mirror("YZ"), op="new", name="Guard, left")
wheel_guards.add("deflector_right", spark, op="new", name="Spark deflector, right")
wheel_guards.add("deflector_left", spark.mirror("YZ"), op="new", name="Spark deflector, left")
wheel_guards.material("aluminum-6061-t6", color="#2a2f3a")
wheel_guards.material("steel-s235jr", bodies=["deflector_right", "deflector_left"], color="#b8bcc2")
