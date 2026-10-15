# Rear end bell

STEP: [`step/end_bell.step`](step/end_bell.step). Source: `source/components/end_bell.py`, design revision 48.

| | |
|---|---|
| Quantity | 1 |
| Material | 6061-T6 |
| Stock | Ø4.25" (108 mm) bar × 20 mm, or from the Ø5" bar |
| Finish | Black anodise Type II. **Mask**: Ø28 bearing seat and its groove, Ø85.10 spigot, tapped holes |
| Process | Lathe op 10 (front: spigot, boss, Ø28 seat, DIN 472 groove, front face), op 20 (rear face, Ø19 hole, OD); then drill and tap from the rear face (C-axis live tooling or a 3-axis mill with the part on its spigot). 2–3 setups |
| General tolerance | ISO 2768-mK; ISO 13715 −0.3 edges |

## Critical features

| Feature | Size and tolerance | Why |
|---|---|---|
| Spigot into the housing bore (datum **B**) | **Ø85.10 g6 (−0.012/−0.034)**, 3 long | Centres the end bell, and so the rear bearing, on the stator bore (Ø85.100 +0.035). 0.5 × 45° lead-in |
| Front (flange) face | Perpendicular to B within 0.02 | Shaft squareness |
| 6001-2RS seat | **Ø28 K7 (+0.006/−0.015)**, floor 2.0 from the rear face; coaxial to B within 0.015; Ra 0.8 | Stationary outer ring in a light-alloy housing: aluminium grows about twice as fast as steel, so take the fit one step tighter than the H7/J7 used in steel. 0.3 × 0.3 corner relief at the floor; 0.5 × 45° lead-in |
| DIN 472 28 groove | **Ø29.4 H11 (+0.13/0)**, width **1.30 +0.14/0**, its rear wall 8.00 +0.05/0 from the seat floor (bearing width 8) | Holds the 6001 outer ring against the floor; 3.7 mm of material ahead of it (n ≥ 2.1) |
| Shaft hole | Ø19 ±0.1 | Clears the DIN 471 ring on the shaft behind the bearing |
| 4 × Ø4.5 + Ø8 counterbore 4.5 deep from the rear face, PCD 92 at 45°/135°/225°/315° | Ø4.5 (ISO 273 normal), cbore Ø8.0 +0.2/0 × 4.5 ±0.1. Position Ø0.2 | ISO 4762 M4 × 16 to the housing; head 0.5 below the face |
| 3 × M3 at R37, 30°/150°/270°, from the rear face | **M3-6H, 8 full thread**, drill Ø2.5 × 9 (+ point). Position Ø0.2 | ISO 7380 M3 × 25 from the rear cap, 8 mm engaged |
| 4 × M2 at R24.5, 0°/60°/120°/180°, from the rear face | **M2-6H, 5 full thread**, drill Ø1.6 × 6 (+ point). **Position Ø0.05** to B and to the 6001 seat | Readhead standoffs: AksIM-2 allows ±0.4 radial and ±0.3 tangential offset of the readhead to the ring |
| Rear face (standoff seat) | Flatness 0.02, perpendicular to B 0.02 | Sets the ring-to-readhead gap (2.88 ±0.13) and tilt (< 0.2°) |

## Inspection

CMM: spigot, seat, groove position, M2 hole positions (they set the encoder alignment). Thread gauges.

## DFM review

| Finding | Change |
|---|---|
| Sharp seat corner, no lead-in | 0.3 × 0.3 relief, 0.5 × 45° lead-ins, outside edge breaks |
| No fasteners to the housing or for the cap | 4 × M4 counterbored, 3 × M3 tapped |
| 6001 outer ring not retained | DIN 472 28 groove in a 3 mm boss ahead of the seat |
| Placeholder read-head mount (encoder area) | Replaced by 4 × M2 holes for the RLS AksIM-2 readhead standoffs |
