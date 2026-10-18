# Output-bearing clamp ring (new part)

STEP: [`step/bearing_clamp.step`](step/bearing_clamp.step). Source: `source/components/bearing_clamp.py`, design revision 49.

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
| OD | **Ø90 js5 (±0.0075)** | Fits the housing counterbore and the flange recess, both Ø90 H6 (+0.022/0): at most 0.030 diametral clearance on each, so together they let the ring gear sit at most 0.030 off the bearing axis (0.069 with g6/H7). The whole stack, with the bearing's own fit and the coaxialities, is about 0.035 typical and 0.08 worst case, against 0.05–0.10 backlash |
| Overall height (bottom face to top face) | **Make 2.70 +0.05/0; finish at assembly** to H = R + d − B + 0.02 (±0.01), from the measured flange recess depth R (1.00), housing seat depth d (11.50) and bearing width B (10.00, ISO 492 normal class 0/−0.12). Nominal parts give 2.52; a bearing at its minimum width gives 2.64 | Sets 0.01–0.03 mm crush on the bearing's outer ring when the flange is screwed down. The bearing's width tolerance (0.12) is far larger than the crush, so the ring is faced to the bearing actually fitted. The housing counterbore floor is 0.25 below the nominal bearing face, so the ring always bears on the bearing, not the floor |
| Inner lip | ID Ø54 ±0.05 (clears the inner ring Ø46 and its seal), lip 1.0 thick from Ø54 to Ø68 | Bears only on the outer ring (Ø49–60 face) |
| Bottom and top faces | Parallel 0.01, flat 0.01 | Even clamping |
| Inner bore of the raised rim | Ø68 +0.1/0 | Clears the carrier plate (Ø66) by 1 mm |
| Edges | 0.3 × 45° on the OD, 0.2 on the lip | |

## DFM review

New part, plain turned ring, no findings. 0.3 / 0.2 × 45° edge breaks modelled.
