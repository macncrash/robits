# Planet carrier, rear part

STEP: [`step/carrier.step`](step/carrier.step). Source: `source/parts/carrier.py` = STEVE part
`06b08578-4496-4595-b037-45ea7c5146a4` revision 8.

| | |
|---|---|
| Quantity | 1 |
| Material | AISI 303 (1.4305), annealed, cold finished (the model shows 304: STEVE's library has no 303) |
| Stock | Ø2.75" (69.85) bar × 37 (the sleeve is now 32.6 long) |
| Finish | Passivate, ASTM A967 (citric or nitric) |
| Process | Lathe op 10 (sleeve OD, DIN 471 groove, shaft clearance bore, rear face); op 20 (plate OD and front face, HK1210 seat, shoulder); 3-axis mill from the front (+Z): posts with a Ø6 R1 bull-nose (leaves the 1 mm post-root fillet), M4 tap drills; co-drill the planet-pin holes with the front disk clamped on. 3 setups |
| General tolerance | ISO 2768-mK; ISO 13715 −0.3 edges |

## Critical features

| Feature | Size and tolerance | Why |
|---|---|---|
| Sleeve, CRBH 3510 inner-ring seat, z 32.5..42.5 (datum **D**) | **Ø35 h5 (0/−0.011)**, Ra 0.4, cylindricity 0.004; 0.5 × 45° lead-in at the rear end | IKO's recommended shaft fit for CRBH with a rotating inner ring, normal load (check the bought bearing's table) |
| Bearing shoulder Ø41, face at z 42.5 | Face perpendicular to D within 0.005; 0.3 × 0.3 relief in the corner | Inner ring banks here; the CRBH's shoulder diameter limit should be checked against IKO's drawing (Ø41 is under the inner ring OD 46) |
| DIN 471 35 groove, z 30.9..32.5 | **Ø33.0 h12 (0/−0.25)**, width **1.60 +0.14/0**; front wall flush with the bearing's rear face (10.00 +0.05/0 from the shoulder face) | Retaining ring holds the inner ring rearward; with the shoulder it fixes the carrier axially |
| HK1210 seat (12 × 16 × 10 drawn cup), z 37..47.5 | **Ø16 N6 (−0.020/−0.009)**, coaxial to D within 0.01, Ra 0.8; 0.5 × 45° lead-in | INA: drawn cups in steel housings (303 counts as steel) need N6; the cup takes its shape from the bore |
| Shaft clearance bore, z 27.9..37 | Ø14 ±0.1 | Clears the Ø12 shaft |
| Front face of the posts (z 60.5) | Flat 0.01 and perpendicular to D 0.01, together | Seats the front disk |
| Rear plate front face (z 47.5) | Perpendicular to D 0.02 | Planets run against it (0.5 mm end gap) |
| 3 × planet-pin holes Ø6 through the plate, at R22.5, 0°/120°/240° | Co-drill Ø5.8 with the front disk clamped on (pins and screws in place), then ream **Ø6 N7 (−0.016/−0.004)** here. True position Ø0.01 to D, pitch circle R22.500 ±0.005 | ISO 8734 6 m6 × 18 hardened pins pressed in. The pin positions set the gear centre distances: ±0.005 keeps the backlash within the budget |
| 3 × M4 in the posts (R22.5, 60°/180°/300°) | **M4-6H, 11.5 full thread**, tap drill Ø3.3 × 13 (118° point, 1 mm of floor left). Position Ø0.1 | ISO 10642 M4 × 16 from the front disk, 11 mm engaged |
| Post-root fillets | R1 (bull-nose cutter) | Lowers the plate stress peak (analysis: rear part 21.6 MPa at the sharp corner) |
| Shoulder-to-plate fillet | R0.4 | README "still open" item; was a sharp corner (stress singularity in the overhung-load study) |

## DFM review (STEVE `cnc` check: 2 setups, no errors at revision 36 or 8)

| Finding | Change |
|---|---|
| Sharp sleeve-to-plate corner (README "still open") | 0.4 fillet (at the new shoulder) |
| Sharp post-to-plate corners | R1 fillets |
| HK1210 seat drawn at Ø18 (HK1210 is 12 × 16 × 10) | Ø16 N6 |
| CRBH inner ring not retained | Ø41 shoulder in front, DIN 471 35 groove behind; sleeve 5.6 mm longer at the back |
| Flat-bottomed tap holes, no edge breaks | 118° drill points, lead-ins and edge breaks |
