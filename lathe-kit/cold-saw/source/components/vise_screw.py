"""Quick-action vise screw, M12, with its lever: flip the lever to free the half-nut and slide the jaw up to the
work, then a quarter turn clamps."""
from steve import Component
from coldsaw_shapes import ycyl, xcyl

s = ycyl(6, -245, -170, -135, 38).fuse(ycyl(10, -245, -232, -135, 38))
s = s.fuse(xcyl(5, -185, -85, -240, 38))
vise_screw = Component("vise_screw", name="Vise screw and lever")
vise_screw.add("screw", s.clean(), name="Vise screw")
vise_screw.material("steel-1c45", finish="polished")
