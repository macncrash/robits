# Planet gear (m1, 27 T), 3 off (+1 spare)

STEP: [`step/planet.step`](step/planet.step) (modelled at its own origin, axis Z, z 0..12). Source:
`source/components/planet.py` and `source/gearing.py`, design revision 48.

**Who makes it:** a gear shop (hob, carburise, grind teeth, grind the bore), as for the sun.

| | |
|---|---|
| Quantity | 3 per actuator, order 4 |
| Material | 18CrNiMo7-6 (or 9310 / 8620 with certificate) |
| Heat treatment | Carburise, 58–62 HRC, Eht 0.3–0.5, core 30–42 HRC |
| Stock | Ø32 bar × 17 each |

## Gear data

| | |
|---|---|
| Module / teeth / α | 1 / 27 / 20°, spur, x = 0, ISO 53 profile A (ρf 0.38) |
| Pitch / tip / root | 27.000 / **29.00 h11** / 24.50 |
| Face width | 12.00 −0.05/−0.10 |
| Span over 4 teeth | W4 = 10.711 nominal; make **10.711 −0.025/−0.045** |
| Over 2 pins Ø1.75 | Md = 29.435 nominal (odd tooth count: measure over pins in opposite gaps) |
| Quality | ISO 1328-1 grade 6, ground |
| Mates with | Sun z 18 (a = 22.5) and ring z 72 (internal) |
| Tooth ends | 0.2 × 45° tip chamfer |

## Other features

| Feature | Size and tolerance | Why |
|---|---|---|
| Bore for the HK0609 drawn cup | **Ø10 N6 (−0.016/−0.007)**, ground after hardening, Ra 0.8, runout to the pitch circle 0.01 | INA/Schaeffler: drawn cups in steel housings need N6 (N7 permissible); the cup takes its shape and running clearance from the bore. 0.3 × 45° lead-ins both sides |
| Faces | Parallel 0.01 | The planet runs between the carrier plates |

The needles run on the planet pins: buy those as **ISO 8734 / DIN 6325 6 m6 × 18, hardened and ground (≥ 58 HRC)**,
not ISO 2338 (unhardened). Note: INA asks for an h6 raceway for normal clearance; an m6 pin (+0.004/+0.012) takes
up some of the cup's clearance. Check the operating clearance with INA, or ask the pin supplier for h6.

## DFM review

| Finding | Decision |
|---|---|
| Sharp tooth roots in the assembly model | ISO 53 root fillet 0.38 m modelled (the hob generates the real one) |
| Teeth not 3-axis millable | Hobbed and ground by a gear shop to the table above |
| Sharp bore edges for a pressed drawn cup | 0.3 × 45° lead-ins |
