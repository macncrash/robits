# Encoder cap (fluted rear cap)

STEP: [`step/rear_cap.step`](step/rear_cap.step). Source: `source/components/rear_cap.py`, design revision 48.

| | |
|---|---|
| Quantity | 1 |
| Material | 6061-T6 |
| Stock | Ø3.5" (88.9 mm) bar × 22 mm |
| Finish | Black anodise Type II (all over; mask nothing) |
| Process | Turn-mill with C-axis and radial live tooling: op 10 turn OD Ø84, face, bore the Ø78 × 14 cavity, leaving 3 internal bosses at R37 (mill them with the cavity, from the front, Ø6 or smaller end mill: R1.5 where they meet the wall); op 20 rear face, Ø10 cable hole, Ø3.4 holes through the bosses, Ø7 cable hole in the rear face. 48 grip flutes: Ø2 end mill, radial, C-axis indexed every 7.5°, 0.8 deep, slots 13.5 long with full-round ends, ending 1.5 from the rear face. |
| General tolerance | ISO 2768-mK; ISO 13715 −0.3 edges |

## Critical features

| Feature | Size and tolerance | Why |
|---|---|---|
| Front face (seats on the end bell) | Flat 0.05 | Seals the cavity |
| Cavity | Ø78 +0.2/0 × 14.0 +0.2/0 | Clears the AksIM-2 readhead (Ø54 arc, top at 11.6–11.9 from the end bell): about 1.4 mm axial margin |
| 3 × Ø3.4 through the bosses at R37 (30°/150°/270°) | Ø3.4 (ISO 273 normal). Position Ø0.2 to the end bell's M3 holes | ISO 7380 M3 × 25 |
| 48 flutes | 2.0 +0.1/0 wide, 0.8 deep, 7.5° pitch | Cosmetic grip. If the look allows, a DIN 82 RAA 1.0 straight knurl on the lathe is cheaper |
| Ø7 encoder cable exit in the rear face at R32, 330° | Ø7 +0.2/0; deburr well, fit a grommet | Readhead cable (Ø6.2); clear of the flutes and of the readhead (R27) |

## DFM review

| Finding | Change |
|---|---|
| 8 faces unreachable and 312 sharp inside corners (square-ended flutes) | Flutes changed to round-ended slots a Ø2 end mill cuts radially |
| No fixing to the end bell | 3 internal bosses with Ø3.4 holes; R1.5 fillets where they meet the cavity wall (first placed tangent to the wall, which left a cusp the check flagged) |
| Flute ends 1.0 from the chamfered rear face left a 0.78 mm lip | Flutes end 1.5 from the rear face |
| Encoder cable had no way out | Ø7 hole in the rear face (a radial hole would have cut through the flutes) |

At revision 48 the check still lists the flutes (96 faces it can't reach from the six 3-axis directions, 24 corners along the radial tool axis, 1.0 mm radii): expected, they are cut radially on the C-axis with a Ø2 end mill. The 0.78 mm thin-wall flag is gone.
