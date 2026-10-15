# Output-bearing clamp ring (new part)

STEP: [`step/bearing_clamp.step`](step/bearing_clamp.step). Source: `source/components/bearing_clamp.py`, design revision 48.

Holds the CRBH 3510 outer ring against the housing seat floor and centres the front flange (and the ring gear) on
the bearing axis. It is captive between the carrier plate and the bearing: slide it over the carrier sleeve
before pressing the bearing on, then fit the DIN 471 35 ring.

| | |
|---|---|
| Quantity | 1 |
| Material | AISI 303 (1.4305) (304 in the model) |
| Stock | Ø95 × 6 disk, or ring from tube |
| Finish | Passivate |
| Process | Lathe, 2 ops (or one op and a part-off with the back faced on a soft-jaw second op) |
| General tolerance | ISO 2768-mK |

| Feature | Size and tolerance | Why |
|---|---|---|
| OD | **Ø90 g6 (−0.012/−0.034)** | Fits the housing counterbore and the flange recess, both Ø90 H7 |
| Overall height (bottom face to top face) | **2.50 +0.03/+0.01** | Crush on the bearing: the housing counterbore is 1.60 deep with its floor 0.10 below the bearing, the flange recess 1.00 deep: 0.01–0.04 mm crush when the flange is screwed down (check at assembly) |
| Inner lip | ID Ø54 ±0.05 (clears the inner ring Ø46 and its seal), lip 1.0 thick from Ø54 to Ø68 | Bears only on the outer ring (Ø49–60 face) |
| Bottom and top faces | Parallel 0.01, flat 0.01 | Even clamping |
| Inner bore of the raised rim | Ø68 +0.1/0 | Clears the carrier plate (Ø66) by 1 mm |
| Edges | 0.3 × 45° on the OD, 0.2 on the lip | |

## DFM review

New part, plain turned ring, no findings. 0.3 / 0.2 × 45° edge breaks modelled.
