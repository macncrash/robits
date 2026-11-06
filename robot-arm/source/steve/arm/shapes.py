"""Small CadQuery helpers: solids placed directly in the design frame (mm)."""
import math
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


def fillet_seams(fused, parts, r, keep=None):
    """Fillet the edges where `parts` meet in `fused` (edges that none of the parts had on its own);
    keep(edge) narrows them, e.g. to the outside seam."""
    def key(e):
        c = e.Center()
        return round(c.x, 2), round(c.y, 2), round(c.z, 2), round(e.Length(), 2)
    old = {key(e) for p in parts for e in p.Edges()}
    seams = [e for e in fused.Edges() if key(e) not in old and (keep is None or keep(e))]
    # Add the seam edges one at a time, keeping each one the kernel can round cleanly with the others:
    # a valid solid, a finite area, about the same volume and no bulge past the unfilleted part.
    vol, area, bb = fused.Volume(), fused.Area(), fused.BoundingBox()

    def sane(s):
        if not s.isValid():
            return False
        a, v, b = s.Area(), s.Volume(), s.BoundingBox()
        return (math.isfinite(a) and 0.8 * area < a < 1.2 * area and abs(v - vol) < 0.02 * vol
                and b.xmin > bb.xmin - 1 and b.ymin > bb.ymin - 1 and b.zmin > bb.zmin - 1
                and b.xmax < bb.xmax + 1 and b.ymax < bb.ymax + 1 and b.zmax < bb.zmax + 1)

    done, out = [], fused
    for e in seams:
        try:
            trial = fused.fillet(r, done + [e])
        except Exception:
            continue
        if sane(trial):
            out = trial
            done.append(e)
    return out, len(done), len(seams)


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
