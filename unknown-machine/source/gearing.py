"""Involute spur and internal gear outlines (20 deg pressure angle), shared by the gears of this design.

Tooth roots get the ISO 53 basic-rack root radius (0.38 x module) so the model matches a hobbed or shaped gear;
the gear shop cuts the teeth to the data table in build-pack/cnc/ (the model's teeth are the reference shape).
"""
import math

import cadquery as cq

PRESSURE_ANGLE = math.radians(20)
ROOT_FILLET = 0.38  # x module: ISO 53 basic rack profile A root radius


def _involute(angle):
    return math.tan(angle) - angle


def gear_points(module, teeth, addendum=1.0, dedendum=1.25, steps=4):
    """Outline of an external spur gear, tooth 0 centred on +X."""
    pitch = module * teeth / 2
    base = pitch * math.cos(PRESSURE_ANGLE)
    tip, root = pitch + addendum * module, pitch - dedendum * module
    start = max(base, root)

    def half(radius):
        return math.pi / (2 * teeth) + _involute(PRESSURE_ANGLE) - _involute(math.acos(base / radius))

    radii = [start + (tip - start) * i / steps for i in range(steps + 1)]
    polar = lambda r, a: (r * math.cos(a), r * math.sin(a))  # noqa: E731
    points = []
    for k in range(teeth):
        centre = 2 * math.pi * k / teeth
        if root < base:
            points.append(polar(root, centre - half(base)))
        points += [polar(r, centre - half(r)) for r in radii]
        points += [polar(r, centre + half(r)) for r in reversed(radii)]
        if root < base:
            points.append(polar(root, centre + half(base)))
        points.append(polar(root, centre + math.pi / teeth))
    return points


def _round_roots(solid, radius, root_r, teeth=None):
    """Fillet the vertical tooth-root corners on the root circle. With `teeth`, skip the vertex in the middle of
    each gap (external gears: it is convex, not a root corner)."""
    edges = []
    for e in solid.Edges():
        a, b = e.startPoint(), e.endPoint()
        if e.geomType() != "LINE" or abs(a.x - b.x) > 1e-6 or abs(a.y - b.y) > 1e-6:
            continue
        if abs(math.hypot(a.x, a.y) - root_r) > 1e-4:
            continue
        if teeth and abs(math.atan2(a.y, a.x) % (2 * math.pi / teeth) - math.pi / teeth) < 1e-4:
            continue
        edges.append(e)
    return solid.fillet(radius, edges)


def spur_gear(module, teeth, width, addendum=1.0, dedendum=1.25, turn=0.0, root_fillet=ROOT_FILLET):
    gear = cq.Workplane("XY").polyline(gear_points(module, teeth, addendum, dedendum)).close().extrude(width)
    if root_fillet:
        root_r = module * teeth / 2 - dedendum * module
        gear = cq.Workplane("XY").newObject([_round_roots(gear.val(), root_fillet * module, root_r, teeth)])
    return gear.rotate((0, 0, 0), (0, 0, 1), turn) if turn else gear


def ring_gear(module, teeth, width, rim, turn=0.0, root_fillet=ROOT_FILLET):
    """Internal gear with a rim `rim` mm outside the tooth roots; a tooth space centred on +X."""
    root_r = module * teeth / 2 + 1.25 * module
    outer = root_r + rim
    blank = cq.Workplane("XY").circle(outer).extrude(width)
    cutter = spur_gear(module, teeth, width + 2, addendum=1.25, dedendum=1.0, turn=turn, root_fillet=0).translate((0, 0, -1))
    ring = blank.cut(cutter)
    if root_fillet:
        ring = cq.Workplane("XY").newObject([_round_roots(ring.val(), root_fillet * module, root_r)])
    return ring
