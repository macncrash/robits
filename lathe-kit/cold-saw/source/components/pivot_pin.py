"""Chop pivot pin, Ø16 ground steel, through the turntable cheeks and the head's knuckle, with a torsion spring
outside each cheek that lifts the head back up when the handle is let go."""
from steve import Component
from coldsaw_shapes import xcyl
from coldsaw_params import pivot_y, pivot_z

pin = xcyl(8, 2, 148, pivot_y, pivot_z)
springs = xcyl(18, 2, 14, pivot_y, pivot_z).fuse(xcyl(18, 136, 148, pivot_y, pivot_z))
springs = springs.cut(xcyl(9, 1, 149, pivot_y, pivot_z))
pivot_pin = Component("pivot_pin", name="Pivot pin and return springs")
pivot_pin.add("pin", pin, name="Pivot pin Ø16")
pivot_pin.add("springs", springs.clean(), name="Torsion springs (2)")
pivot_pin.material("steel-1c60", finish="polished")
