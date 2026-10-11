"""Small CadQuery helpers shared by the components (solids about the Z axis, boxes, bearings)."""
import math

import cadquery as cq


def cyl(r, h, z, x=0.0, y=0.0):
    return cq.Solid.makeCylinder(r, h, cq.Vector(x, y, z), cq.Vector(0, 0, 1))


def ring(ro, ri, h, z):
    return cyl(ro, h, z).cut(cyl(ri, h, z))


def box(x0, y0, z0, x1, y1, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def xcyl(r, x0, x1, y, z):
    return cq.Solid.makeCylinder(r, x1 - x0, cq.Vector(x0, y, z), cq.Vector(1, 0, 0))


def turned(shape, degrees):
    return shape.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), degrees)


def ball_bearing(ri, ro, w, z):
    """Outer race, inner race and a ring of balls for a deep-groove bearing, bore ri, OD ro, width w."""
    t = 0.28 * (ro - ri)
    outer = ring(ro, ro - t, w, z)
    inner = ring(ri + t, ri, w, z)
    pr, br = (ri + ro) / 2, 0.2 * (ro - ri)
    n = int(2 * math.pi * pr / (2.5 * br))
    balls = [cq.Solid.makeSphere(br, cq.Vector(pr * math.cos(2 * math.pi * k / n), pr * math.sin(2 * math.pi * k / n), z + w / 2),
                                 cq.Vector(0, 0, 1), -90, 90, 360) for k in range(n)]
    return outer, inner, cq.Compound.makeCompound(balls)
