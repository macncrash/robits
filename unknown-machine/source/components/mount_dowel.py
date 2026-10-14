"""ISO 2338 dowel pin 4 m6 x 12 locating the housing in the pedestal saddle (modelled along +Y from the origin)."""
import cadquery as cq
from steve import Component

mount_dowel = Component("mount_dowel", name="Dowel pin ISO 2338 4x12 (pedestal)")
pin = cq.Workplane("XZ").circle(2).extrude(-12).faces(">Y or <Y").chamfer(0.4).val()
mount_dowel.add("pin", pin, name="Pin")
mount_dowel.material("steel-1c60", finish="polished")
