"""Small CadQuery helpers: solids placed directly in the design frame (mm)."""
import cadquery as cq

V = cq.Vector
AXES = {"X": (1, 0, 0), "Y": (0, 1, 0), "Z": (0, 0, 1)}


def cyl(r, center, axis, length):
    """Cylinder of radius r and the given length, centred on `center`, along axis X/Y/Z."""
    d = V(*AXES[axis])
    return cq.Solid.makeCylinder(r, length, V(*center) - d * (length / 2), d)


def ring(ro, ri, center, axis, length):
    return cyl(ro, center, axis, length).cut(cyl(ri, center, axis, length + 1))


def box(sx, sy, sz, center, fillet_z=0):
    wp = cq.Workplane("XY").box(sx, sy, sz).translate(center)
    if fillet_z:
        wp = wp.edges("|Z").fillet(fillet_z)
    return wp.val()


def fuse(*solids):
    out = solids[0]
    for s in solids[1:]:
        out = out.fuse(s)
    return out.clean()


def rot_y(solid, pivot, degrees):
    return solid.rotate(V(*pivot), V(*pivot) + V(0, 1, 0), degrees)


def finger(side, x0, y0, z_top):
    """One claw finger, open position. side = -1 (left, -X) or +1 (right). Returns (finger, pad, pin)."""
    s = side
    carriage = box(26, 40, 12, (x0 + 53 * s, y0, z_top - 6))
    plate = box(12, 34, 60, (x0 + 46 * s, y0, z_top - 42))
    knuckle_z = z_top - 72
    tip = box(10, 30, 44, (x0 + 46 * s, y0, knuckle_z - 22))
    tip = tip.cut(box(12, 32, 10, (x0 + 49 * s, y0, knuckle_z - 44), 0))  # chamfer-like relief at the tip
    pad = box(4, 26, 30, (x0 + 39 * s, y0, knuckle_z - 22))
    tilt = 12 * s
    tip = rot_y(tip, (x0 + 46 * s, y0, knuckle_z), tilt)
    pad = rot_y(pad, (x0 + 46 * s, y0, knuckle_z), tilt)
    body = fuse(carriage, plate, tip, cyl(10, (x0 + 46 * s, y0, knuckle_z), "Y", 30))
    pin = cyl(5, (x0 + 46 * s, y0, knuckle_z), "Y", 40)
    return body.cut(cyl(5, (x0 + 46 * s, y0, knuckle_z), "Y", 40)), pad, pin
