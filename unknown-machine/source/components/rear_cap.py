"""Knurled encoder cover on the back of the end bell, with the hollow-shaft cable exit."""
from steve import Component
from shapes import cyl, box, turned

rear_cap = Component("rear_cap", name="Encoder cap (knurled)")
cap = cyl(42, 17, -65).cut(cyl(39, 14, -62)).cut(cyl(5, 4, -66))
for k in range(48):
    cap = cap.cut(turned(box(41.2, -0.9, -64, 43, 0.9, -50), 7.5 * k))
rear_cap.add("cap", cap.clean(), name="Cap")
rear_cap.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
