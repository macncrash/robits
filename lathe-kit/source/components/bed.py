"""Bed: 6061 bar with a 55-degree male dovetail on top (Sherline-style flat bed), 500 long, 100 wide, 45 tall.

The ways are the dovetail: 80 wide at the top (z -98), undercut to 66 at z -108, shoulders out to 100 below.
Carriage and tailstock ride on it with brass gibs. Hard-anodise the ways (or fit steel way strips) for wear.
"""
from steve import Component
from lathe_shapes import prism_yz, zcyl
from lathe_params import bed_x0, bed_len

top, neck = -98, -108
profile = [(-40, top), (40, top), (33, neck), (50, neck), (50, -143), (-50, -143), (-50, neck), (-33, neck)]
bed = prism_yz(profile, bed_x0, bed_x0 + bed_len)
for x in (-20, 70):                                  # M6 tapped for the headstock plate
    for y in (-25, 25):
        bed = bed.cut(zcyl(2.5, top - 12, top, x, y))
for x in (20, 410):                                  # M8 tapped for the feet
    for y in (-30, 30):
        bed = bed.cut(zcyl(3.4, -143, -128, x, y))
bed_c = Component("bed", name="Bed (dovetail ways)")
bed_c.add("bed", bed.clean(), name="Bed")
bed_c.material("aluminum-6061-t6", finish="anodized", color="#15171c")
