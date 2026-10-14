"""Drive hub, AISI 303: the disc sander's hub pattern on the actuator's output disk (6 x M4 x 12 into its load
holes, Ø20 pilot), with a Ø19 stub for the jaw coupling to the worm's input shaft. 304 stands in for 303."""
import math

from steve import Component
from coldsaw_shapes import ycyl
from coldsaw_params import gear_x, worm_z, act_y

y_back = act_y - 65.5
y_front = y_back - 20
hub = ycyl(40, y_front, y_back, gear_x, worm_z)
hub = hub.cut(ycyl(40.5, y_back - 2, y_back, gear_x, worm_z)).fuse(ycyl(34, y_back - 2, y_back, gear_x, worm_z))
hub = hub.cut(ycyl(10, y_back - 6.8, y_back, gear_x, worm_z))
for k in range(6):
    a = math.radians(60 * k + 30)
    x, z = gear_x + 25 * math.cos(a), worm_z + 25 * math.sin(a)
    hub = hub.cut(ycyl(2.25, y_front, y_back, x, z)).cut(ycyl(4.0, y_front, y_back - 8, x, z))
hub = hub.fuse(ycyl(9.5, y_front - 25, y_front, gear_x, worm_z))
drive_hub = Component("drive_hub", name="Drive hub (303)")
drive_hub.add("hub", hub.clean(), name="Drive hub")
drive_hub.material("stainless-304", finish="machined")
