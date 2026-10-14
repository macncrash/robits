"""Small CadQuery helpers for the band saw (saw frame: blade's cutting run at x 0 along Z, teeth toward -Y, Z up,
mm).

Named bandsaw_shapes (not shapes) so it can't clash with the linked actuator's own shapes module.
"""
import math

import cadquery as cq


def box(x0, y0, z0, x1, y1, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def xcyl(r, x0, x1, y=0.0, z=0.0):
    return cq.Solid.makeCylinder(r, x1 - x0, cq.Vector(x0, y, z), cq.Vector(1, 0, 0))


def ycyl(r, y0, y1, x=0.0, z=0.0):
    return cq.Solid.makeCylinder(r, y1 - y0, cq.Vector(x, y0, z), cq.Vector(0, 1, 0))


def zcyl(r, z0, z1, x=0.0, y=0.0):
    return cq.Solid.makeCylinder(r, z1 - z0, cq.Vector(x, y, z0), cq.Vector(0, 0, 1))


def prism_xz(points, y0, y1):
    """A prism along Y from a polygon of (x, z) points (the XZ workplane extrudes toward -Y)."""
    return cq.Workplane("XZ", origin=(0, y1, 0)).polyline(points).close().extrude(y1 - y0).val()


def tilt_point(r, a):
    """(x, z) at radius r from the table's tilt axis (y axis through x 0, z 0), angle a in degrees from straight
    down toward +X."""
    return (r * math.sin(math.radians(a)), -r * math.cos(math.radians(a)))


def tilt_sector(r0, r1, a0, a1, y0, y1, n=30):
    """Annular sector about the tilt axis, along Y."""
    pts = [tilt_point(r1, a0 + (a1 - a0) * k / n) for k in range(n + 1)]
    pts += [tilt_point(r0, a1 - (a1 - a0) * k / n) for k in range(n + 1)]
    return prism_xz(pts, y0, y1)


def one(*shapes):
    """Several solids as one body. STEVE's per-body mesh export keeps only a component's first body, so each
    component here is a single body (a compound where it has separate pieces)."""
    return cq.Compound.makeCompound([s for s in shapes])


def ring_xz(cx, cz, r0, r1, a0, a1, y0, y1, n=96):
    """Annular sector about an axis along Y through (cx, cz), angles from +X toward +Z. The inner edge's chords
    are pushed out to touch the true r0 circle (so a band drawn round a wheel never cuts into it)."""
    r0 = r0 / math.cos(math.radians((a1 - a0) / n / 2))
    pts = [(cx + r1 * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
            cz + r1 * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]
    pts += [(cx + r0 * math.cos(math.radians(a1 - (a1 - a0) * k / n)),
             cz + r0 * math.sin(math.radians(a1 - (a1 - a0) * k / n))) for k in range(n + 1)]
    return prism_xz(pts, y0, y1)


def wheel(cz, shaft_y1):
    """Band wheel about an axis along Y through (125, cz): cast 6061 centre (rim, web with six windows, hub), and
    a Ø10 x 2 mm crowned-flat urethane tyre to Ø250, separately; shaft Ø20 from the hub back to shaft_y1.
    Returns (centre, tyre)."""
    cx = 125
    rim = ycyl(119, -8, 8, cx, cz).cut(ycyl(108, -9, 9, cx, cz))
    web = ycyl(108.5, -3, 3, cx, cz)
    for k in range(6):
        a = math.radians(60 * k + 30)
        web = web.cut(ycyl(26, -4, 4, cx + 68 * math.cos(a), cz + 68 * math.sin(a)))
    hub = ycyl(24, -14, 14, cx, cz)
    shaft = ycyl(10, 13, shaft_y1, cx, cz)
    centre = rim.fuse(web).fuse(hub).fuse(shaft).clean()
    tyre = ycyl(125, -10, 10, cx, cz).cut(ycyl(119, -11, 11, cx, cz))
    return centre, tyre
