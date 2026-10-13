"""Rotor: hollow motor shaft (8 mm cable bore), rotor hub and 14 surface magnets."""
from steve import Component
from shapes import ring, box, turned

rotor = Component("rotor", name="Rotor + hollow shaft")
rotor.add("shaft", ring(6, 4, 120, -60), name="Hollow shaft")
hub = ring(26, 6, 4, -28).fuse(ring(26, 23, 36, -24))
rotor.add("hub", hub.clean(), op="new", name="Rotor hub")
magnets = ring(27.4, 26, 36, -24)
for k in range(14):
    magnets = magnets.cut(turned(box(25.9, -0.3, -25, 27.5, 0.3, 13), 360 / 14 * k))
rotor.add("magnets", magnets, op="new", name="Magnets")
rotor.material("steel-s235jr", finish="machined")
rotor.material("steel-s235jr", bodies=["magnets"], color="#8a8f99")  # NdFeB grade SH (150 C) or UH (180 C): not in the library, steel stand-in
