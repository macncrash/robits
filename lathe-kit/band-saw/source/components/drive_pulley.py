"""Drive pulley, AISI 303 hub with an HTD 8M 20-tooth, 30 mm pulley (pitch Ø50.93, outside Ø49.56) and two
flanges, bolted to the actuator's output disk like the lathe's chuck backplate: Ø20 pilot over the output hub, 6 x
M4 x 12 into the load holes (put in before the pulley body goes on; the pulley is a stock taper-lock 20T on the
hub's spigot in practice). Modelled in the saw frame on the actuator axis (x 125, z motor_z); the output face is
y 45."""
from steve import Component
from bandsaw_shapes import ycyl
from bandsaw_params import motor_z

z = motor_z
plate = ycyl(40, 45, 53, 125, z).cut(ycyl(40.5, 45, 47, 125, z).cut(ycyl(34, 45, 47, 125, z)))
plate = plate.cut(ycyl(10, 45, 51.8, 125, z))                                # pilot over the output hub
teeth = ycyl(49.56 / 2, 55, 85, 125, z)
flanges = ycyl(30, 53, 55, 125, z).fuse(ycyl(30, 85, 87, 125, z))
pulley = plate.fuse(teeth).fuse(flanges).cut(ycyl(6, 52, 88, 125, z))
drive_pulley = Component("drive_pulley", name="Drive pulley HTD 8M 20T on a 303 hub")
drive_pulley.add("pulley", pulley.clean(), name="Pulley 20T and hub")
drive_pulley.material("stainless-304", finish="machined")   # specified AISI 303 hub, steel pulley
