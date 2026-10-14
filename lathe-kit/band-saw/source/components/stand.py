"""Stand: welded frame of 40 x 40 x 3 box section, 10 mm top plate, 6 mm lower shelf, four levelling feet (M12,
Ø50 pads). Puts the table top at 1000 mm. Bolt it to the floor or load the shelf. Powder coated."""
from steve import Component
from bandsaw_shapes import box, zcyl, one
from bandsaw_params import stand_top, floor_z

leg_bottom = floor_z + 15
plate = box(-80, -170, stand_top - 10, 370, 170, stand_top)


def shs(x0, y0, z0, x1, y1, z1, axis):
    outer = box(x0, y0, z0, x1, y1, z1)
    i = {"x": (x0 - 1, y0 + 3, z0 + 3, x1 + 1, y1 - 3, z1 - 3), "y": (x0 + 3, y0 - 1, z0 + 3, x1 - 3, y1 + 1, z1 - 3),
         "z": (x0 + 3, y0 + 3, z0 - 1, x1 - 3, y1 - 3, z1 + 1)}[axis]
    return outer.cut(box(*i))


legs_x, legs_y = ((-70, -30), (320, 360)), ((-160, -120), (120, 160))
frame = None
for xs in legs_x:
    for ys in legs_y:
        leg = shs(xs[0], ys[0], leg_bottom, xs[1], ys[1], stand_top - 10, "z")
        foot = box(xs[0] - 5, ys[0] - 5, leg_bottom - 5, xs[1] + 5, ys[1] + 5, leg_bottom)
        frame = leg.fuse(foot) if frame is None else frame.fuse(leg).fuse(foot)
for z0 in (stand_top - 50, floor_z + 120):
    for ys in legs_y:
        frame = frame.fuse(shs(-30, ys[0], z0, 320, ys[1], z0 + 40, "x"))
    for xs in legs_x:
        frame = frame.fuse(shs(xs[0], -120, z0, xs[1], 120, z0 + 40, "y"))
shelf = box(-70, -160, floor_z + 160, 360, 160, floor_z + 166)
for xs in legs_x:
    for ys in legs_y:
        shelf = shelf.cut(box(xs[0], ys[0], floor_z + 159, xs[1], ys[1], floor_z + 167))
pads = None
for x in (-50, 340):
    for y in (-140, 140):
        pad = zcyl(25, floor_z, floor_z + 8, x, y).fuse(zcyl(6, floor_z + 8, leg_bottom - 5, x, y))
        pads = pad if pads is None else pads.fuse(pad)
stand = Component("stand", name="Stand")
stand.add("stand", one(plate, frame.clean(), shelf.clean(), pads.clean()),
          name="Top plate 450 x 340 x 10, 40 x 40 x 3 SHS frame, shelf, M12 levelling feet")
stand.material("steel-s235jr", color="#2b2f36")
