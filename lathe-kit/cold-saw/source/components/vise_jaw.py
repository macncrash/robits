"""Moving vise jaw on its slide beam, closed on the Ø40 bar: the quick-action screw pushes it from the front."""
from steve import Component
from coldsaw_shapes import box, ycyl
from coldsaw_params import table_z

jaw = box(-160, -60, table_z + 0.5, -35, -40, 75).fuse(box(-145, -200, table_z + 0.5, -125, -60, 45))
jaw = jaw.cut(ycyl(6, -200.5, -170, -135, 38))                              # M12 nut thread in the beam
vise_jaw = Component("vise_jaw", name="Moving vise jaw")
vise_jaw.add("jaw", jaw.clean(), name="Moving jaw")
vise_jaw.material("steel-1c45", finish="machined", color="#5a5f66")
