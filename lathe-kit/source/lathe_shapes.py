"""Small CadQuery helpers for the lathe kit (lathe frame: spindle along +X, Z up, operator at -Y, mm).

Named lathe_shapes (not shapes) so it can't clash with the linked actuator's own shapes module.
"""
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

