"""Frameless BLDC stator: laminated core with 12 slots, pressed into the housing bore."""
from steve import Component
from shapes import ring, box, turned

stator = Component("stator", name="Stator core")
core = ring(42, 28, 36, -24)
for k in range(12):
    core = core.cut(turned(box(28.5, -2.5, -25, 36, 2.5, 13), 30 * k + 15))
stator.add("core", core.clean(), name="Laminations")
stator.material("steel-s235jr", color="#5b5f66")
