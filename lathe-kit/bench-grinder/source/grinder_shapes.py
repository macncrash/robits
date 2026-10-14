"""Small CadQuery helpers for the bench grinder (spindle along X at y 0, z = spindle_z; Z up; operator at -Y)."""
import math
import cadquery as cq
from grinder_params import spindle_z


def box(x0, y0, z0, x1, y1, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def xcyl(r, x0, x1, y=0.0, z=spindle_z):
    return cq.Solid.makeCylinder(r, x1 - x0, cq.Vector(x0, y, z), cq.Vector(1, 0, 0))


def ycyl(r, y0, y1, x=0.0, z=spindle_z):
    return cq.Solid.makeCylinder(r, y1 - y0, cq.Vector(x, y0, z), cq.Vector(0, 1, 0))


def zcyl(r, z0, z1, x=0.0, y=0.0):
    return cq.Solid.makeCylinder(r, z1 - z0, cq.Vector(x, y, z0), cq.Vector(0, 0, 1))


def xring(r_out, r_in, x0, x1):
    """A tube on the spindle axis."""
    return xcyl(r_out, x0, x1).cut(xcyl(r_in, x0 - 1, x1 + 1))


def prism_yz(points, x0, x1):
    """A prism along X from a polygon of (y, z) points."""
    return cq.Workplane("YZ", origin=(x0, 0, 0)).polyline(points).close().extrude(x1 - x0).val()


def prism_xz(points, y0, y1):
    """A prism along Y from a polygon of (x, z) points."""
    return cq.Workplane("XZ", origin=(0, y1, 0)).polyline(points).close().extrude(y1 - y0).val()


def polar(r, a):
    """(y, z) of a point at radius r from the spindle, a degrees up from the operator's horizontal (-Y)."""
    return (-r * math.cos(math.radians(a)), spindle_z + r * math.sin(math.radians(a)))


def wedge(a0, a1, x0, x1, r=200.0):
    """The sector of space between a0 and a1 degrees (up from -Y) about the spindle, x0..x1."""
    n = max(2, int((a1 - a0) / 5) + 1)
    pts = [(0.0, spindle_z)] + [polar(r, a0 + (a1 - a0) * k / (n - 1)) for k in range(n)]
    return prism_yz(pts, x0, x1)


def sector(r_out, r_in, a0, a1, x0, x1):
    """Part of a tube on the spindle axis between a0 and a1 degrees."""
    return xring(r_out, r_in, x0, x1).intersect(wedge(a0, a1, x0 - 1, x1 + 1, 1.5 * r_out))


def hex_x(across_flats, x0, x1):
    """A hexagon prism on the spindle axis."""
    return cq.Workplane("YZ", origin=(x0, 0, spindle_z)).polygon(6, across_flats / math.cos(math.pi / 6)) \
        .extrude(x1 - x0).val()
