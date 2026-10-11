"""Involute spur-gear outlines (20 deg pressure angle), shared by the gears of this design."""
import math

import cadquery as cq

PRESSURE_ANGLE = math.radians(20)


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


def spur_gear(module, teeth, width, addendum=1.0, dedendum=1.25, turn=0.0):
    gear = cq.Workplane("XY").polyline(gear_points(module, teeth, addendum, dedendum)).close().extrude(width)
    return gear.rotate((0, 0, 0), (0, 0, 1), turn) if turn else gear


def ring_gear(module, teeth, width, rim, turn=0.0):
    """Internal gear with a rim `rim` mm outside the tooth roots; a tooth space centred on +X."""
    outer = module * teeth / 2 + 1.25 * module + rim
    blank = cq.Workplane("XY").circle(outer).extrude(width)
    cutter = spur_gear(module, teeth, width + 2, addendum=1.25, dedendum=1.0, turn=turn).translate((0, 0, -1))
    return blank.cut(cutter)
