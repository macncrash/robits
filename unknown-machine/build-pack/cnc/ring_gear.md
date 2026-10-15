# Ring gear (m1, 72 T internal)

STEP: [`step/ring_gear.step`](step/ring_gear.step) (assembled position, z 48..60). Source:
`source/components/ring_gear.py` and `source/gearing.py`, design revision 48.

**Who makes it:** a gear shop: turn the ring blank, shape the teeth (Fellows / gear shaper) or, for one or two
prototypes, wire-EDM them. No catalogue m1 72 T internal gear exists (see `../hardware/gears.md`).

| | |
|---|---|
| Quantity | 1 |
| Material | 34CrNiMo6 +QT (1.6582), 28–34 HRC before cutting; US alternative AISI 4340. Gas nitriding optional (≥ 550 HV surface, Nht 0.2–0.3) |
| Stock | Ø90 bar or a thick-wall ring blank × 17 |
| General tolerance | ISO 2768-mK |

## Gear data

| | |
|---|---|
| Module / teeth / α | 1 / 72 internal / 20°, spur, x = 0, ISO 53 profile A (root radius 0.38) |
| Pitch / tip (inside) / root | 72.000 / **70.00 H11** / 74.50 |
| Face width | 12.00 −0.05/−0.10 |
| Between 2 pins Ø1.68 | Mi = 69.703 nominal (even teeth: opposite gaps); make **69.703 +0.03/+0.06** (space widening for backlash) |
| Quality | ISO 1328-1 grade 7 (shaped) |
| Mates with | 3 planets z 27 |
| Tooth ends | 0.2 × 45° tip chamfer |

## Other features

| Feature | Size and tolerance | Why |
|---|---|---|
| OD (press fit in the front flange) | **Ø86 s6 (+0.093/+0.071)**, Ra 0.8; runout to the pitch circle 0.015; 0.5 × 45° lead-in chamfers both ends | 0.036–0.093 interference in the flange's Ø86 H7, plus Loctite 638. The aluminium flange loses about 0.05 mm of interference at +50 K, so the compound carries the torque when hot (16 N·m ring reaction; the joint holds hundreds of N·m). Hoop stress in the flange at the maximum interference is about 30 MPa |
| Faces | Parallel 0.01, perpendicular to the OD 0.01 | Rear face seats on the flange lip |

Note for the gear shop: the press fit squeezes the ring's teeth inward by roughly 0.02 mm on the diameter. Either
size the pin measurement for it or check Mi after pressing into the flange.

## DFM review

| Finding | Decision |
|---|---|
| Sharp tooth roots in the assembly model | 0.38 m root fillet modelled |
| Internal teeth not 3-axis millable | Shaped (or wire-EDM) by a gear shop, to the table |
| OD corners sharp | 0.5 × 45° press lead-ins |
