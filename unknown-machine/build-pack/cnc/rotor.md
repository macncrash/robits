# Motor shaft and rotor hub sleeve (two parts, one STEP)

STEP: [`step/rotor.step`](step/rotor.step) holds both bodies: the hollow shaft (z −60..60) and the hub sleeve
(z −17..15.15). Source: `source/components/rotor.py`, design revision 48.

## 1. Hollow shaft

| | |
|---|---|
| Quantity | 1 |
| Material | 42CrMo4 +QT (AISI 4140 pre-hardened, 28–32 HRC). The model shows 34CrNiMo6 as a stand-in (no 42CrMo4 in STEVE's library). Alternative for full needle-raceway hardness: 16MnCr5 / 8620 carburised 58–62 HRC, case 0.5–0.8 |
| Stock | Ø0.5" (12.7) 4140 HT ground bar won't clean up to a ground Ø12 with margin: use Ø16 bar × 130 |
| Finish | Black oxide or light oil, except the ground journals |
| Heat treatment | Induction-harden the HK1210 journal (z 37–47) to **≥ 55 HRC** (4140 rarely reaches 58: INA's load ratings then drop by its hardness factor, about 0.8 at 55 HRC, which is fine for this lightly loaded pilot). If 58 HRC is wanted, use the carburising grade above |
| Process | Turn between centres (Ø16 bar): rough OD, drill the Ø8 bore **from both ends, 60 mm each (7.5 × D, long-series drill or gun drill)**, finish-turn, cut the two DIN 471 grooves, mill the double-D flats (2 ops on a mill or C/Y-axis on a turn-mill), induction-harden, grind the journals. 2 lathe ops + 1 milling op + grinding |
| General tolerance | ISO 2768-mK; ends chamfered 0.5 × 45° inside and out |

| Feature | Size and tolerance | Why |
|---|---|---|
| 6001-2RS inner-ring seat, z −46..−38 | **Ø12 k5 (+0.009/+0.001)**, Ra 0.4 | Rotating inner ring (circumferential load): k5 per the usual SKF table for light loads |
| HK1210 needle raceway, z 37..47 | **Ø12 h6 (0/−0.011)**, ≥ 55 HRC (see above), Ra 0.2, roundness 0.003 | INA: raceway shaft h6 for normal radial clearance in a drawn cup |
| Hub sleeve seat, z −17..15.15 | **Ø12 p6 (+0.029/+0.018)** | Press fit of the hub sleeve (plus Loctite 638) |
| Sun seat and flats, z 47.5..60 | Round portions Ø12 g6 (−0.006/−0.017); **flats 10.80 −0.01/−0.03 across**, symmetric to the axis within 0.02, parallel 0.01 | Double-D drive for the sun (replaces the impossible 4 × 4 key). Sliding fit so the sun slides off forward; the sun bore is 10.80 +0.02/0 |
| DIN 471 12 grooves, z −47.1..−46 and −38..−36.9 | **Ø11.5 h11 (0/−0.11)**, width **1.10 +0.14/0**; inner walls flush with the bearing faces ±0.02 | Hold the 6001 inner ring both ways (the shaft's only axial location). 1.75 mm wall left over the Ø8 bore |
| Encoder hub seat, z −58..−48.5 | Ø12 g6 | Encoder hub (Ø12 H7, Loctite 638) |
| Ø8 cable bore | Ø8 +0.2/0, straightness 0.1 over 120; deburred, no sharp edges inside | Cable pass-through. Where the two drillings meet a step of up to 0.1 is acceptable; deburr it |
| Runout of all seats to the 6001 and HK1210 journals | 0.01 | Rotor air gap and gear mesh |

## 2. Rotor hub sleeve

| | |
|---|---|
| Quantity | 1 |
| Material | C45E +N (1.1191). Not critical magnetically (the KBM rotor has its own steel hub) |
| Stock | Ø38 bar × 37 |
| Finish | Black oxide (mask the bonding surface) |
| Process | Lathe, 2 ops |

| Feature | Size and tolerance | Why |
|---|---|---|
| Bore | **Ø12 H7 (+0.018/0)** | Press onto the shaft's p6 seat with Loctite 638 |
| Rotor seat | **Ø30.000 −0.010/−0.030** (rotor bore 30.010): 0.02–0.04 diametral clearance, Ra 1.6 (not polished) | Kollmorgen bonding clearance for the rotor (Hysol EA 934NA, room-temperature cure, < 82 °C outside the stator) |
| Shoulder Ø34, face at z −15 | Face perpendicular to the bore within 0.01; 0.3 × 0.3 relief in the corner | The rotor banks on it; Ø34 stays below the magnet diameter (Kollmorgen catalog p. 94) |

## DFM review

| Finding | Change / decision |
|---|---|
| Ø8 × 120 bore is 15 × D (over the ~10 × D of standard drills) | Kept (it's the cable pass-through). Drill from both ends, or gun-drill |
| S235 shaft can't be a needle raceway | Material changed to 42CrMo4 + induction-hardened journal (or 16MnCr5 carburised) |
| Sun "keyed" but no key: a 4 × 4 key breaks through the 18 T root | Double-D flats, 10.8 across |
| 6001 not located on the shaft | Two DIN 471 12 × 1 grooves |
| No chamfers, sharp shoulder | 0.5 × 45° ends; 0.3 × 0.3 relief at the rotor shoulder; lead-ins on the sleeve |
