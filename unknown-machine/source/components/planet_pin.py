"""ISO 2338 dowel pin 6 m6 x 18, hardened: planet axle pressed into the carrier (modelled at the origin, z 0..18)."""
import cadquery as cq
from steve import Component

planet_pin = Component("planet_pin", name="Dowel pin ISO 2338 6x18 (planet axle)")
pin = cq.Workplane("XY").circle(3).extrude(18).faces(">Z or <Z").chamfer(0.5).val()
planet_pin.add("pin", pin, name="Pin")
planet_pin.material("steel-1c60", finish="polished")
