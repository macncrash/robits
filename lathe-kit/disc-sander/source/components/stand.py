"""Bench stand: welded open frame of 40 x 40 x 3 steel box section, 10 mm top plate, 6 mm lower shelf, four
levelling feet (M12, Ø50 pads). Puts the table top at 875 mm and the disc centre at 895 mm; bolt it to the floor
or load the shelf. Powder coated.
"""
from steve import Component
from sander_shapes import box, zcyl
from sander_params import base_z, riser_h, top_t, floor_z

top = base_z - riser_h                               # z -158: stand top surface
leg_bottom = floor_z + 15
plate = box(-230, -240, top - top_t, 230, 160, top)


def shs(x0, y0, z0, x1, y1, z1, axis):
    """40 x 40 x 3 box section along an axis."""
    outer = box(x0, y0, z0, x1, y1, z1)
    i = {"x": (x0 - 1, y0 + 3, z0 + 3, x1 + 1, y1 - 3, z1 - 3), "y": (x0 + 3, y0 - 1, z0 + 3, x1 - 3, y1 + 1, z1 - 3),
         "z": (x0 + 3, y0 + 3, z0 - 1, x1 - 3, y1 - 3, z1 + 1)}[axis]
    return outer.cut(box(*i))


frame = None
for xs in ((-220, -180), (180, 220)):
    for ys in ((-230, -190), (110, 150)):
        leg = shs(xs[0], ys[0], leg_bottom, xs[1], ys[1], top - top_t, "z")
        foot = box(xs[0] - 5, ys[0] - 5, leg_bottom - 5, xs[1] + 5, ys[1] + 5, leg_bottom)
        frame = leg.fuse(foot) if frame is None else frame.fuse(leg).fuse(foot)
for z0 in (top - top_t - 40, floor_z + 120):         # rails under the top and under the shelf
    for ys in ((-230, -190), (110, 150)):
        frame = frame.fuse(shs(-180, ys[0], z0, 180, ys[1], z0 + 40, "x"))
    for xs in ((-220, -180), (180, 220)):
        frame = frame.fuse(shs(xs[0], -190, z0, xs[1], 110, z0 + 40, "y"))
shelf = box(-220, -230, floor_z + 160, 220, 150, floor_z + 166)
for xs in ((-220, -180), (180, 220)):               # notch the shelf round the legs
    for ys in ((-230, -190), (110, 150)):
        shelf = shelf.cut(box(xs[0], ys[0], floor_z + 159, xs[1], ys[1], floor_z + 167))
pads = None
for x in (-200, 200):
    for y in (-210, 130):
        pad = zcyl(25, floor_z, floor_z + 8, x, y).fuse(zcyl(6, floor_z + 8, leg_bottom - 5, x, y))
        pads = pad if pads is None else pads.fuse(pad)
stand = Component("stand", name="Bench stand")
stand.add("top_plate", plate, name="Top plate 460 x 400 x 10")
stand.add("frame", frame.clean(), name="Frame (40 x 40 x 3 SHS)")
stand.add("shelf", shelf.clean(), name="Shelf")
stand.add("feet", pads.clean(), name="Levelling feet M12")
stand.material("steel-s235jr", color="#2b2f36")      # powder coated
stand.material("steel-s235jr", bodies=["feet"], color="#8a8f99")
