"""Small CadQuery helpers for the disc sander (sander frame: disc axis along -Y, Z up, operator at -Y, mm).

Named sander_shapes (not shapes) so it can't clash with the linked actuator's own shapes module.
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


def arc_points(cx, cy, r, a0, a1, n=24):
    """Points on an arc about (cx, cy), angles in degrees from +first axis toward +second axis."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def sector_xz(r0, r1, a0, a1, y0, y1):
    """Annular sector about the Y axis (the disc axis), angles in the XZ plane from +X toward +Z, along Y."""
    pts = arc_points(0, 0, r1, a0, a1) + arc_points(0, 0, r0, a1, a0)
    return prism_xz(pts, y0, y1)


def trunnion_point(r, a, py, pz):
    """(y, z) at radius r and angle a (degrees below the -Y direction) from the tilt axis at (py, pz)."""
    return (py - r * math.cos(math.radians(a)), pz - r * math.sin(math.radians(a)))


def sector_yz(r0, r1, a0, a1, py, pz, x0, x1):
    """Annular sector about the table's tilt axis (along X at y py, z pz), angles below -Y, along X."""
    pts = [trunnion_point(r1, a0 + (a1 - a0) * k / 24, py, pz) for k in range(25)]
    pts += [trunnion_point(r0, a1 - (a1 - a0) * k / 24, py, pz) for k in range(25)]
    return prism_yz(pts, x0, x1)
