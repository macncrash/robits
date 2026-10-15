# Encoder hub (new part)

STEP: [`step/encoder_hub.step`](step/encoder_hub.step). Source: `source/components/encoder_hub.py`, design revision 48.

Carries the RLS AksIM-2 ring MRA039BC020DSE00 on the rear end of the motor shaft (see
`../hardware/decisions.md`).

| | |
|---|---|
| Quantity | 1 |
| Material | AISI 303 (1.4305). Non-magnetic matters here: keep magnetic steel away from the ring's magnet |
| Stock | Ø32 bar × 14 |
| Finish | Passivate |
| Process | Lathe, 2 ops (bore, pilot and flange face in one op); drill and tap 8 × M2 and the M2 set-screw hole on a mill or with C-axis live tooling. 2–3 setups |
| General tolerance | ISO 2768-mK; ISO 13715 −0.2 edges |

| Feature | Size and tolerance | Why |
|---|---|---|
| Bore (datum **G**) | **Ø12 H7 (+0.018/0)** | On the shaft's Ø12 g6 seat with Loctite 638 |
| Ring pilot, 1.8 long | **Ø20 g6 (−0.007/−0.020)**, coaxial to G within 0.01 | RLS recommends g6 for the ring's Ø20 H7 bore; radial offset budget ±0.4 total |
| Ring mounting face (flange rear face) | Axial runout to G **≤ 0.01**; flat 0.005 | RLS: tilt < 0.2°, gap 2.88 ±0.13 to the readhead |
| Flange front face | Parallel to the mounting face 0.02; flange thickness 4.00 ±0.02 | Sets the ring's axial position: fit the hub with a 0.50 mm shim against the end bell's rear face while the Loctite cures |
| 8 × M2 through the flange, PCD 25, 22.5° + 45° k | **M2-6H through (4 mm)**, position Ø0.05 to G | ISO 7046 M2 × 6 countersunk ring screws, 4 mm engaged (2 d) |
| M2 set-screw hole, radial through the flange at 0° | M2-6H | DIN 913 M2 × 3 cup point, with Loctite |
| Collar behind the ring | Ø18 0/−0.1, to 9.5 from the flange front face | Must pass through the readhead's Ø21.2 bore |

## DFM review

| Finding | Change |
|---|---|
| 0.43 mm wall around an M3 set-screw hole in the short collar | Set screw moved to the flange, M2 (1.2 mm walls) |
| Ø1.6 radial drilling is 5.7 × D (it runs through to the bore) | Kept: only the outer 4 mm is tapped; a stub drill from the OD to the bore is fine |
| Faces the 3-axis check can't reach | Turned features (lathe part) |
