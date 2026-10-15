"""Motor shaft: hollow shaft (8 mm cable bore) with the hub sleeve the KBM rotor bonds to.

The sleeve is 30 mm (slip fit in the rotor's 30.010 mm bore, bonded) with a 34 mm shoulder the rotor banks
against; the shoulder stays below the magnet diameter, as Kollmorgen asks (catalog p. 94). A relief groove at
the shoulder lets the rotor bank square. The shaft is 42CrMo4 (4140) with an induction-hardened, ground journal
under the HK1210 needles; the sleeve is C45, pressed and bonded on. The sun is driven by two flats (10.8 across,
z 47.5..60, a double-D) and slides off forward; two DIN 471 12 x 1 grooves hold the 6001 inner ring.
CNC notes: build-pack/cnc/rotor.md.
"""
from steve import Component
from shapes import ring, box, edge_break

rotor = Component("rotor", name="Motor shaft + rotor hub sleeve")
shaft = ring(6, 4, 120, -60)
for r, out in ((6, -1), (4, 1)):                     # end chamfers, outside and bore
    for z, up in ((-60, 1), (60, -1)):
        shaft = shaft.cut(edge_break(r, z, 0.5, out, up))
shaft = shaft.cut(box(5.4, -7, 47.5, 7, 7, 61)).cut(box(-7, -7, 47.5, -5.4, 7, 61))   # double-D drive for the sun
for z in (-47.1, -38):                               # DIN 471 12 x 1 grooves (Ø11.5 x 1.1) either side of the 6001
    shaft = shaft.cut(ring(6.5, 5.75, 1.1, z))
rotor.add("shaft", shaft.clean(), name="Hollow shaft")
hub = ring(15, 6, 32.15, -17).fuse(ring(17, 6, 2, -17))   # sleeve z -17..15.15, shoulder z -17..-15
hub = hub.cut(ring(15.3, 14.7, 1.1, -15.3))                # relief 0.3 x 0.3 at the shoulder the rotor banks on
for r, z, size, out, up in ((15, 15.15, 0.5, -1, -1),      # lead-in for the KBM rotor
                            (17, -17, 0.3, -1, 1), (17, -15, 0.3, -1, -1),
                            (6, -17, 0.3, 1, 1), (6, 15.15, 0.3, 1, -1)):   # bore lead-ins for pressing on
    hub = hub.cut(edge_break(r, z, size, out, up))
rotor.add("hub", hub.clean(), op="new", name="Rotor hub sleeve")
rotor.material("steel-34crnimo6", bodies=["shaft"], finish="ground")   # 42CrMo4 / 4140 QT specified; 34CrNiMo6 stand-in
rotor.material("steel-1c45", bodies=["hub"], finish="machined")
