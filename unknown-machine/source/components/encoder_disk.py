"""Encoder code disk on the motor shaft (read at its rim)."""
from steve import Component
from shapes import ring, box, turned

encoder_disk = Component("encoder_disk", name="Encoder disk")
disk = ring(22, 6, 1, -57)
for k in range(64):
    disk = disk.cut(turned(box(19, -0.4, -57.5, 21, 0.4, -55.5), 360 / 64 * k))
encoder_disk.add("disk", disk.clean(), name="Code disk")
encoder_disk.material("stainless-304", finish="polished")
