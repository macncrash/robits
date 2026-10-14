"""Disc hub, AISI 303: the chuck backplate's pattern made deeper. Pilots on the actuator's Ø20 output hub and
bolts to the output disk with 6 x ISO 4762 M4 x 12 in its six load holes (PCD 50, head seat y -73, tip y -61);
the platen bolts to its front face with 6 x M5 countersunk screws on PCD 66. 20 thick, so the platen sits 10 mm in
front of the pedestal and clear of the guard's back wall. The library has no 303, so 304 stands in.
"""
import math

from steve import Component
from sander_shapes import ycyl
from sander_params import disk_face, hub_t

y_back, y_front = -disk_face, -disk_face - hub_t
hub = ycyl(40, y_front, y_back)
hub = hub.cut(ycyl(40.5, y_back - 2, y_back)).fuse(ycyl(34, y_back - 2, y_back))   # relief over the front flange
hub = hub.cut(ycyl(10, y_back - 6.8, y_back))                                      # Ø20 H7 pilot over the output hub
hub = hub.cut(ycyl(8, y_front, y_back))                                            # Ø16 through bore
for k in range(6):
    a = math.radians(60 * k + 30)                    # M4 clearance and Ø8 counterbore from the front
    x, z = 25 * math.cos(a), 25 * math.sin(a)
    hub = hub.cut(ycyl(2.25, y_front, y_back, x, z)).cut(ycyl(4.0, y_front, -73, x, z))
    b = math.radians(60 * k)                         # M5 tapped (4.2 drill) 10 deep for the platen screws
    hub = hub.cut(ycyl(2.1, y_front, y_front + 10, 33 * math.cos(b), 33 * math.sin(b)))
sander_hub = Component("sander_hub", name="Disc hub (303)")
sander_hub.add("hub", hub.clean(), name="Hub Ø80 x 20")
sander_hub.material("stainless-304", finish="machined")   # specified AISI 303 (1.4305); 304 stand-in
