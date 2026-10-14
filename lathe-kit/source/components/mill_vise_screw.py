"""Vise screw M10 with a tommy bar (branch "milling"), into the moving jaw."""
from steve import Component
from lathe_shapes import ycyl, xcyl
from lathe_params import carriage_x

xc = carriage_x + 35
screw = ycyl(5, -112, -64, xc, -30).fuse(ycyl(8, -120, -112, xc, -30))
bar = xcyl(3, xc - 40, xc + 40, -116, -30)
mill_vise_screw = Component("mill_vise_screw", name="Vise screw and bar")
mill_vise_screw.add("screw", screw.fuse(bar).clean(), name="Vise screw")
mill_vise_screw.material("steel-1c60", finish="machined")
