"""Motor shaft: hollow shaft (8 mm cable bore) with the hub sleeve the KBM rotor bonds to.

The sleeve is 30 mm (slip fit in the rotor's 30.010 mm bore, bonded) with a 34 mm shoulder the rotor banks
against; the shoulder stays below the magnet diameter, as Kollmorgen asks (catalog p. 94).
"""
from steve import Component
from shapes import ring

rotor = Component("rotor", name="Motor shaft + rotor hub sleeve")
rotor.add("shaft", ring(6, 4, 120, -60), name="Hollow shaft")
hub = ring(15, 6, 32.15, -17).fuse(ring(17, 6, 2, -17))   # sleeve z -17..15.15, shoulder z -17..-15
rotor.add("hub", hub.clean(), op="new", name="Rotor hub sleeve")
rotor.material("steel-s235jr", finish="machined")
