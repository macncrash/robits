"""Moving jaw of the milling vise (branch "milling"), closed on the 30-wide workpiece."""
from steve import Component
from lathe_shapes import box, ycyl
from lathe_params import carriage_x

xc = carriage_x + 35
jaw = box(xc - 30, -74, -44, xc + 30, -60.05, -16).cut(ycyl(5.1, -75, -61, xc, -30))
mill_vise_jaw = Component("mill_vise_jaw", name="Vise moving jaw")
mill_vise_jaw.add("jaw", jaw.clean(), name="Moving jaw")
mill_vise_jaw.material("steel-1c60", finish="machined", color="#5a5f66")
