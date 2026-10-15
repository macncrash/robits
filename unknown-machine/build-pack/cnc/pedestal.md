# Pedestal

STEP: [`step/pedestal.step`](step/pedestal.step). Source: `source/parts/pedestal.py` = STEVE part
`0a76af67-d956-4543-8c69-fc7a041b5f47` revision 8. Frame: the actuator's (axis Z, pedestal toward −Y).

| | |
|---|---|
| Quantity | 1 |
| Material | 6061-T6 (T6511 plate or rectangle bar) |
| Stock | 2.5" × 6" (63.5 × 152.4) rectangle bar × 4.25" (108) long |
| Finish | Black anodise Type II. **Mask** the saddle bores (thermal joint; chromate conversion there) and the dowel holes |
| Process | 3-axis mill, 4–5 setups: (1) base underside (−Y up): face, 4 × Ø9 bolt holes, 4 counterbores Ø9.5 and Ø5.5 holes; (2) top (+Y): base plate top, block outline, Ø4 dowel holes through the saddle bottom; (3) part on end (+Z up): **saddle Ø120 by circular interpolation** (or boring head) to z 14, the step face, chamfer; (4) −Z up: saddle Ø96; (5) cable slot from ±X (Ø8 end mill from both sides). A 4th axis or horizontal mill combines 3–5 |
| General tolerance | ISO 2768-mK; ISO 13715 −0.3 edges |

## Critical features

| Feature | Size and tolerance | Why |
|---|---|---|
| Saddle bore under the front section (datum **F**) | **Ø120 +0.03/0**, z 14..44; cylindricity 0.02; Ra 1.6 | Housing Ø120 g6: 0.012–0.064 clearance, filled with thermal paste. (README mentions a 0.25 mm pad: it would need about Ø120.5; decide pad or paste before machining) |
| Saddle bore under the fins | **Ø96 +0.03/0**, coaxial with F within 0.02 | Fin tips Ø96 g6 |
| Step face at z 14 | 0.5 × 45° chamfer on its inner edge | Clears the housing's 0.5 chamfer at the Ø120/Ø96 step |
| 2 × Ø4 dowel holes, on the centre line at z 22 and 40 | **Ø4 N7 (−0.004/−0.016)**, 6 deep from the saddle (drilled 7 + point); position ±0.01 to each other and to F | ISO 8734 4 m6 dowels pressed in; the housing's matching holes are H7 slip. Leave an air vent or press slowly (blind holes) |
| 4 × Ø5.5 + Ø9.5 counterbores from below, x ±16, z 28 / 37 | Ø5.5 (ISO 273 normal); cbore Ø9.5 × to y −66 (22 deep); position Ø0.2 to the dowels | ISO 4762 M5 × 20 into the housing. The Ø5.5 holes break out through the curved saddle surface with a feather edge: deburr. (STEVE's thin-wall flag, 0.24 mm, is this edge) |
| 4 × Ø9 base holes | Ø9 ±0.1, position Ø0.3 | M8 to the user's structure |
| Base underside | Flat 0.05 | Heat path to the structure |
| Cable slot | 8 × 14 with R4 ends, through in X; ±0.2 | Ø8 end mill from each side (41 mm reach, 5 × D) or drill Ø8 twice and mill the web |

## DFM review (STEVE `cnc` check, revision 7 → 8)

| Finding | Change |
|---|---|
| 5 sharp inside corners in the cable port (a square tunnel along X) | Port changed to a round-ended slot a Ø8 end mill leaves |
| Thin wall 0.24 mm at the screw holes | Left as is: the clearance holes exit a curved surface, the sliver is the exit edge. Deburr |
| Sharp saddle step meeting the housing's corner | 0.5 × 45° chamfer |
| Flat-bottomed dowel holes | Drill points modelled |
