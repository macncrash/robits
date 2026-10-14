"""Small CadQuery helpers for the cold saw (saw frame: stock along X, blade in the YZ plane, operator at -Y, Z up,
mm). Named coldsaw_shapes (not shapes) so it can't clash with the linked actuator's own shapes module.
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


def prism_xy(points, z0, z1):
    """A prism along Z from a polygon of (x, y) points."""
    return cq.Workplane("XY", origin=(0, 0, z0)).polyline(points).close().extrude(z1 - z0).val()


def blade_point(r, phi, yc, zc):
    """(y, z) at radius r about the blade axis (yc, zc); phi in degrees from the -Y (front) direction toward +Z."""
    return (yc - r * math.cos(math.radians(phi)), zc + r * math.sin(math.radians(phi)))


def sector_x(r0, r1, a0, a1, yc, zc, x0, x1, n=36):
    """Annular sector about an X axis through (yc, zc), angles as blade_point, extruded along X."""
    pts = [blade_point(r1, a0 + (a1 - a0) * k / n, yc, zc) for k in range(n + 1)]
    pts += [blade_point(r0, a1 - (a1 - a0) * k / n, yc, zc) for k in range(n + 1)]
    return prism_yz(pts, x0, x1)


def sector_z(r0, r1, a0, a1, z0, z1, n=36):
    """Annular sector about the Z axis, angles in degrees from -Y toward +X, extruded along Z."""
    def pt(r, a):
        return (r * math.sin(math.radians(a)), -r * math.cos(math.radians(a)))
    pts = [pt(r1, a0 + (a1 - a0) * k / n) for k in range(n + 1)]
    pts += [pt(r0, a1 - (a1 - a0) * k / n) for k in range(n + 1)]
    return prism_xy(pts, z0, z1)
