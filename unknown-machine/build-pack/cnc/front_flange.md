# Front flange

STEP: [`step/front_flange.step`](step/front_flange.step). Source: `source/components/front_flange.py`, design revision 48.

| | |
|---|---|
| Quantity | 1 |
| Material | 6061-T6 |
| Stock | Ø5" bar × 26 (from the housing's bar) |
| Finish | Black anodise Type II (the model shows a slightly bluer black). **Mask**: Ø86 ring-gear bore, Ø90 recess, rear face |
| Process | Lathe op 10 (rear: face, Ø90 recess, lip bore Ø78); op 20 (front: Ø86 bore, relief, front face, OD); drill the 4 counterbored holes (C-axis or 3-axis mill). 2–3 setups |
| General tolerance | ISO 2768-mK; ISO 13715 −0.3 edges |

## Critical features

| Feature | Size and tolerance | Why |
|---|---|---|
| Ø90 recess in the rear face (datum **C**) | **Ø90 H7 (+0.035/0)**, depth **1.00 +0.01/−0.01** | Fits over the bearing clamp ring (Ø90 g6), which sits in the housing's Ø90 H7 counterbore: centres the flange and ring gear on the bearing axis, and the recess floor presses the clamp ring onto the bearing |
| Ring-gear bore | **Ø86 H7 (+0.035/0)**, coaxial to C within 0.015, Ra 0.8; 0.5 × 45° lead-in at the front; 0.3 × 0.3 relief at the lip | Press fit of the ring gear (Ø86 s6). Turn the Ø86 bore and the Ø90 recess in one setup if possible, or hold the part on C for op 20 |
| Lip face at z 48 (ring gear seat) | Perpendicular to C within 0.02 | Ring gear squareness |
| Rear face (on the housing) | Flat 0.02, parallel to the lip face 0.02 | |
| 4 × Ø5.5 thru + Ø9.5 × 5.5 counterbore, PCD 100 at 45°/135°/225°/315° | Ø5.5 (ISO 273 normal) ; cbore Ø9.5 +0.2/0 × 5.5 ±0.1; position Ø0.2 to C | ISO 4762 M5 × 30 into the housing |

## Assembly note

Press the ring gear in from the front with Loctite 638, against the lip. Clamp-ring crush: with the flange
screwed down, the flange's recess floor should press the clamp ring 0.01–0.04 mm onto the bearing. Check with a
feeler gauge under the flange before the screws are tightened fully (gap 0.01–0.04 at the flange face), and lap the
clamp ring's top face if there is no gap.

## DFM review

| Finding | Change |
|---|---|
| Located only by the 4 screws in Ø5.5 holes (±0.25 mm of float at the ring gear) | Ø90 H7 recess over the clamp ring centres it |
| Sharp corner where the ring gear seats | 0.3 × 0.3 relief |
| No lead-in for the press fit, sharp OD edges | 0.5 × 45° chamfers |
