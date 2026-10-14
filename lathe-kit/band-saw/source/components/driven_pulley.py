"""Driven pulley, HTD 8M 100 teeth for a 30 mm belt (pitch Ø254.65, outside Ø253.28), 6061, on the lower wheel's
shaft behind the frame (keyed, set screw): rim, a web with six windows and a hub. Teeth drawn as their outside
diameter."""
import math

from steve import Component
from bandsaw_shapes import ycyl
from bandsaw_params import lower_z

r_od = 253.28 / 2
rim = ycyl(r_od, 55, 85, 125, lower_z).cut(ycyl(r_od - 14, 54, 86, 125, lower_z))
web = ycyl(r_od - 13, 66, 74, 125, lower_z)
for k in range(6):
    a = math.radians(60 * k)
    web = web.cut(ycyl(25, 65, 75, 125 + 70 * math.cos(a), lower_z + 70 * math.sin(a)))
hub = ycyl(25, 53, 87, 125, lower_z)
pulley = rim.fuse(web).fuse(hub).cut(ycyl(10, 52, 88, 125, lower_z))
driven_pulley = Component("driven_pulley", name="Driven pulley HTD 8M 100T")
driven_pulley.add("pulley", pulley.clean(), name="Pulley 100T")
driven_pulley.material("aluminum-6061-t6", finish="machined")
