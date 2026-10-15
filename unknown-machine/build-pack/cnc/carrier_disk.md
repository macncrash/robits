# Planet carrier, front disk and output hub

STEP: [`step/carrier_disk.step`](step/carrier_disk.step). Source: `source/parts/carrier_disk.py` = STEVE part
`d93731cc-e121-4579-99c7-86e726295491` revision 5.

| | |
|---|---|
| Quantity | 1 |
| Material | AISI 303 (1.4305) |
| Stock | Ø2.75" bar × 16 |
| Finish | Passivate, ASTM A967 |
| Process | Lathe op 10 (back face, OD), op 20 (front face, Ø20 output pilot with its relief, Ø8 bore); then drill/countersink/tap on a mill (or C-axis): 3 countersunk holes, 6 × M4, and the 3 pin holes co-drilled with the rear part. 2–3 setups |
| General tolerance | ISO 2768-mK; ISO 13715 −0.3 edges |

## Critical features

| Feature | Size and tolerance | Why |
|---|---|---|
| Back face (on the posts, datum **E**) | Flat 0.01 | |
| Output pilot (hub) | **Ø20 g6 (−0.007/−0.020)**, coaxial with the pin-hole circle within 0.01; 0.3 × 0.3 relief at the root; 0.5 × 45° lead-in | Pilots the arm (or the lathe chuck backplate's Ø20 H7 bore) |
| Front (output) face, z 65.5 | Parallel to E within 0.01 | Arm mounting face |
| 3 × Ø6 pin holes, 2 deep, R22.5 at 0°/120°/240° | Co-drilled with the rear part; ream **Ø6 H7 (+0.012/0)**, flat bottom (end mill), depth 2.0 +0.1/0 | Locates the disk on the planet pins (slip fit here, press in the rear plate) |
| 3 × Ø4.5 + 90° countersink Ø9.0, R22.5 at 60°/180°/300° | Countersink Ø9.0–9.2 so the ISO 10642 M4 head (Ø8.96 max) sits flush to 0.2 below | |
| 6 × M4 through, R25 at 30° + 60° k | **M4-6H through 5 mm**, position Ø0.1 to the pilot | Arm load holes |
| Ø8 cable bore | Ø8 +0.1/0 | |

## DFM review (STEVE `cnc` check)

| Finding | Change |
|---|---|
| Sharp corner at the pilot root (mating parts need a clean shoulder) | 0.3 × 0.3 turned relief (the check lists its undercut face as unreachable on a 3-axis mill: it is a lathe grooving operation) |
| Sharp edges | 0.5 / 0.3 × 45° chamfers |
