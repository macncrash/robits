"""Rear end bell: closes the can, carries the rear bearing and the encoder readhead standoffs.

The 6001-2RS outer ring sits on the seat floor and is held by a DIN 472 28 x 1.2 ring (groove in a short boss
ahead of the seat); the inner ring is held on the shaft by two DIN 471 12 x 1 rings. Four ISO 4762 M4 x 16 screws in
counterbores hold it to the housing; the rear cap screws into it (3 x M3) and the four readhead standoffs screw
into M2 holes in its rear face. Turned in two ops, then drilled. CNC notes: build-pack/cnc/end_bell.md.
"""
import math

from steve import Component
from shapes import ring, cyl, edge_break, drill_point

end_bell = Component("end_bell", name="Rear end bell")
bell = cyl(51.5, 12, -48).fuse(ring(42.55, 30, 3, -36))          # disk z -48..-36, spigot into the housing (stator) bore
bell = bell.fuse(ring(17.5, 14, 3, -36))                          # boss z -36..-33 carrying the DIN 472 groove
bell = bell.cut(cyl(14, 13, -46)).cut(cyl(9.5, 14, -49))          # 6001 seat Ø28 z -46..-33; Ø19 hole (clears the shaft circlip)
bell = bell.cut(ring(14.7, 13.9, 1.3, -38))                       # DIN 472 28 groove: Ø29.4 x 1.3, against the bearing's front face
bell = bell.cut(ring(14.3, 13.7, 1.1, -46.3))                     # corner relief 0.3 x 0.3 at the 6001 seat floor
for r, z, size, out, up in ((14, -33, 0.5, 1, -1),      # lead-in: 6001 seat entry
                            (17.5, -33, 0.3, -1, -1),   # boss
                            (42.55, -33, 0.5, -1, -1),  # lead-in: spigot
                            (51.5, -48, 0.5, -1, 1),    # rear face OD
                            (51.5, -36, 0.5, -1, -1)):  # front face OD
    bell = bell.cut(edge_break(r, z, size, out, up))
for k in range(4):                                      # 4 x Ø4.5 + Ø8 x 4.5 counterbores, PCD 92, for ISO 4762 M4 x 16
    a = math.radians(45 + 90 * k)
    x, y = 46 * math.cos(a), 46 * math.sin(a)
    bell = bell.cut(cyl(2.25, 14, -49, x, y)).cut(cyl(4, 6, -49.5, x, y))
for k in range(3):                                      # 3 x M3 tapped (2.5 drill, 9 deep) at R37 for the rear-cap screws
    a = math.radians(30 + 120 * k)
    x, y = 37 * math.cos(a), 37 * math.sin(a)
    bell = bell.cut(cyl(1.25, 9, -48, x, y)).cut(drill_point(1.25, (x, y, -39), (0, 0, 1)))
for k in range(4):                                      # 4 x M2 tapped (1.6 drill, 6 deep) at R24.5 for the readhead standoffs
    a = math.radians(60 * k)
    x, y = 24.5 * math.cos(a), 24.5 * math.sin(a)
    bell = bell.cut(cyl(0.8, 6, -48, x, y)).cut(drill_point(0.8, (x, y, -42), (0, 0, 1)))
end_bell.add("bell", bell.clean(), name="End bell")
end_bell.material("aluminum-6061-t6", finish="anodized", color="#1b2030")
