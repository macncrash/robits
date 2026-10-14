"""Small CadQuery helpers for the lathe kit (lathe frame: spindle along +X, Z up, operator at -Y, mm).

Named lathe_shapes (not shapes) so it can't clash with the linked actuator's own shapes module.
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


def prism_yz(points, x0, x1):
    """A prism along X from a polygon of (y, z) points."""
    return cq.Workplane("YZ", origin=(x0, 0, 0)).polyline(points).close().extrude(x1 - x0).val()


def prism_xz(points, y0, y1):
    """A prism along Y from a polygon of (x, z) points (the XZ workplane extrudes toward -Y)."""
    return cq.Workplane("XZ", origin=(0, y1, 0)).polyline(points).close().extrude(y1 - y0).val()


def ring_marks(r, z0, count, every, short, long_, depth=0.4, width=0.35, span=360.0, start=0.0):
    """Engraved index lines on the outside of a cylinder about Z: `count` lines over `span` degrees from `start`,
    each `short` long along Z from z0 (every `every`-th one `long_`). Returns one solid to cut."""
    lines = None
    step = span / count
    n = count + (0 if span >= 360 else 1)
    for k in range(n):
        length = long_ if k % every == 0 else short
        line = box(r - depth, -width / 2, z0, r + 1, width / 2, z0 + length)
        line = line.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), start + k * step)
        lines = line if lines is None else lines.fuse(line)
    return lines



# --- Ball screws (SFU1204: Ø12, 4 mm lead, Ø2.5 balls) and their nuts ---
BALL_LEAD = 4.0


def ball_screw(z0, z1, journals=()):
    """SFU1204 shaft along +Z, grooved from z0 to z1 at the 4 mm lead, with plain Ø10 journals given as
    (z_from, z_to) pairs next to it. One revolved solid: the round ball groove is drawn as a ring every lead
    rather than a helix (STEVE's kernel returns no solid when a helical sweep is cut into the shaft), which
    looks the same at the drawing's scale and leaves the screw's size, travel and lead exact."""
    phi0 = math.acos(0.2 / 1.35)                     # groove (r 1.35 about r 6.2) meets the Ø12 crest
    spans = sorted([(z0, z1, None)] + [(a, b, 5.0) for a, b in journals])
    pts = [(0, spans[0][0])]
    for a, b, r in spans:
        if r is not None:
            pts += [(r, a), (r, b)]
            continue
        pts.append((6, a))
        n = int((b - a) // BALL_LEAD)
        first = a + (b - a - n * BALL_LEAD) / 2 + BALL_LEAD / 2
        for k in range(n):
            zc = first + k * BALL_LEAD
            for i in range(9):
                phi = -phi0 + 2 * phi0 * i / 8
                pts.append((6.2 - 1.35 * math.cos(phi), zc + 1.35 * math.sin(phi)))
        pts.append((6, b))
    pts.append((0, spans[-1][1]))
    clean = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - clean[-1][0]) > 1e-6 or abs(p[1] - clean[-1][1]) > 1e-6:
            clean.append(p)
    return cq.Workplane("XZ").polyline(clean).close().revolve(360, (0, 0, 0), (0, 1, 0)).val()


def ball_nut():
    """SFU1204 flanged ball nut along +Z from z 0: Ø24 body 30 long, Ø40 x 10 flange at z 30..40 with the
    catalogue's single flat 10 mm off the axis on +Y, 4 x Ø4.5 on PCD 32, wiper seals at both ends."""
    body = cq.Solid.makeCylinder(12, 30, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))
    body = body.cut(cq.Solid.makeCylinder(13, 1.2, cq.Vector(0, 0, 4), cq.Vector(0, 0, 1)).cut(
        cq.Solid.makeCylinder(11.4, 1.2, cq.Vector(0, 0, 4), cq.Vector(0, 0, 1))))    # seal-retainer groove
    flange = cq.Solid.makeCylinder(20, 10, cq.Vector(0, 0, 30), cq.Vector(0, 0, 1))
    flange = flange.cut(box(-21, 10, 29, 21, 21, 41))
    for a in (30, 150, 210, 330):
        x, y = 16 * math.cos(math.radians(a)), 16 * math.sin(math.radians(a))
        flange = flange.cut(cq.Solid.makeCylinder(2.25, 10, cq.Vector(x, y, 30), cq.Vector(0, 0, 1)))
    nut = body.fuse(flange)
    return nut.cut(cq.Solid.makeCylinder(6.05, 40, cq.Vector(0, 0, 0), cq.Vector(0, 0, 1))).clean()


def handwheel_solid(dial_r, lines, every):
    """Handwheel with a graduated dial along +Z from its mounting face at the origin: Ø16 hub, dial ring of
    `lines` engraved lines (long every `every`), Ø70 wheel with three lightening holes and a crank."""
    hub = zcyl(8, 0, 2)
    dial = zcyl(dial_r, 2, 14).cut(ring_marks(dial_r, 2, lines, every, 3.0, 5.5))
    wheel = zcyl(35, 14, 20)
    for k in range(3):
        a = 120 * k + 60
        wheel = wheel.cut(zcyl(8, 14, 20, 22, 0).rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), a))
    crank = zcyl(4, 20, 38, 27, 0).fuse(zcyl(6.5, 38, 52, 27, 0))
    return hub.fuse(dial).fuse(wheel).fuse(crank).cut(zcyl(5, -1, 21)).clean()


def way_cover(x_near, x_far):
    """Printed way cover (PETG or ASA, 2.4 mm walls) running from a carriage end face (x_near) out to x_far:
    a roof 2.4 mm over the dovetail ways, side skirts, a shelf over the leadscrew, and an end wall that clears
    the bed by 1 mm (stick a felt wiper strip inside it). Two tabs with M4 clearance holes screw it to the
    carriage end. Print it standing on its carriage end (tabs and wall edges flat on the plate): no supports;
    about 40 x 150 x 40 mm."""
    x0, x1 = min(x_near, x_far), max(x_near, x_far)
    shell = None
    for y0, z0, y1, z1 in ((-64.4, -95.6, 64.4, -93.2), (62, -106, 64.4, -93.2), (-64.4, -108, -62, -93.2),
                           (-86, -110.4, -62, -107.9), (-86, -118, -83.6, -110.3)):
        part = prism_yz([(y0, z0), (y1, z0), (y1, z1), (y0, z1)], x0, x1)
        shell = part if shell is None else shell.fuse(part)
    xe0, xe1 = (x1 - 3, x1) if x_far > x_near else (x0, x0 + 3)
    end = prism_yz([(-86, -118), (64.4, -118), (64.4, -93.2), (-86, -93.2)], xe0, xe1)
    end = end.cut(prism_yz([(-41, -97), (41, -97), (34, -107), (51, -107), (51, -150), (-51, -150), (-51, -107),
                            (-34, -107)], xe0 - 1, xe1 + 1))
    end = end.cut(xcyl(7, xe0 - 1, xe1 + 1, -67.5, -120))
    xt0, xt1 = (x_near, x_near + 4) if x_far > x_near else (x_near - 4, x_near)
    for y in (-40, 40):
        tab = box(xt0, y - 10, -95.6, xt1, y + 10, -80).cut(xcyl(2.2, xt0 - 1, xt1 + 1, y, -86))
        shell = shell.fuse(tab)
    return shell.fuse(end).clean()
