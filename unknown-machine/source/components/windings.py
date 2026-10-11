"""Copper windings: a coil side in each stator slot plus the two end-turn bundles."""
from steve import Component
from shapes import ring, box, turned

windings = Component("windings", name="Windings")
cu = ring(38, 30, 6, -30).fuse(ring(38, 30, 6, 12))
for k in range(12):
    cu = cu.fuse(turned(box(29.2, -2.2, -24, 35.8, 2.2, 12), 30 * k + 15))
windings.add("coils", cu.clean(), name="Coils")
windings.material("copper-c10200", color="#b8733a")
