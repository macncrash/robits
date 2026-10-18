# Fit check before cutting steel: the housing and plastic gears

Before the gears are ordered, mill the housing, make the flange, clamp ring and carrier, and print the gears in
plastic. That proves the assembly order, the clearances and that the ring gear goes on over the planets. It
does **not** prove backlash, noise or mesh quality: those come from the steel gears' tolerances (AM-13 to AM-15).

Source: STEVE design 02e31a10 revision 49. These limits come from the tolerance-stack review on 2026-10-17;
`cnc/README.md` explains the changes it made.

## 1. Buy these before finishing any bore

| Part | Why it comes first |
|---|---|
| Kollmorgen KBM-17H01-B00 (or at least its outline drawing) | The model's stator bore (Ø52) and rotor OD (Ø50) are **estimates**: the real air gap isn't known. Rough the housing's stator bore about 0.5 under and finish it to the stator in hand (Ø85.100 +0.035 against a catalogue OD of 84.963). The hub sleeve (AM-10) needs the real rotor bore |
| IKO CRBH 3510 A UU | Its width (10.00, ISO 492 normal class 0/−0.12) sets the clamp ring's height. Its OD (60, 0/−0.013) is what the Ø60 H7 seat fits |
| INA HK1210 and 3 × HK0609 drawn cups | The cups take their shape from their bores: check the N6 bores with the cup pressed in, using a pin gauge for the needles' inner diameter |

## 2. The tolerances that matter most, in order

| # | Feature | Limit | What it controls |
|---|---|---|---|
| 1 | Housing: Ø60 seat and Ø90 counterbore coaxial to the stator bore A | 0.015 | Motor air gap and gear centre. The two bores are cut from opposite ends: in op 20 hold the part on A (expanding mandrel) or dial A in to 0.005 or better, then finish Ø60, its floor, Ø90 and the front face without unclamping |
| 2 | Ø90 H6 counterbore (housing), Ø90 H6 recess (flange), Ø90 js5 clamp ring | +0.022/0, ±0.0075 | How far the ring gear can sit off the carrier axis. These two fits together allowed 0.069 mm radial with g6/H7, now 0.030. With the bearing's fit and the coaxialities, the whole stack is about 0.035 typical, 0.08 worst case (was 0.055 / 0.12). Each 0.01 off-centre takes about 0.007 from one planet's backlash: the centring step at assembly takes most of it out |
| 3 | Ø60 H7 seat: diameter, floor depth 11.50 −0.02, floor square to A 0.015, Ra 0.8 | | Bearing fit; the floor depth is one term in the clamp-ring stack |
| 4 | Stator bore Ø85.100 +0.035, cylindricity 0.02, adhesive grooves 0.20 ±0.05, ledge square to A 0.03 | | Bonded stator: concentric, square and bonded over enough length |
| 5 | Front face flat and square to A | 0.02 | Flange and ring-gear squareness |
| 6 | Carrier: pin circle R22.500 ±0.005, true position Ø0.01; Ø35 h5 sleeve; HK1210 seat coaxial 0.01 | | Gear centre distance. A printed carrier can't hold these: use the 303 carrier |
| 7 | Dowel holes (housing to pedestal) | ±0.01 | Easier to drill the housing and pedestal together, or open one hole into a slot |

## 3. Machining the housing: be careful with

- **Thin wall under the fins.** Use soft or pie jaws and light finishing passes. Check the bore's roundness after
  unclamping, not while clamped.
- **Temperature.** Aluminium grows about 2 µm per °C on Ø85. A part measured 5 °C warm reads 0.01 large, a third
  of the bore tolerance. Measure at 20 °C after the part has cooled.
- **Radial holes.** They start on a surface inclined at 15.5°. Spot each one with a Ø5 flat end mill first.
- **Anodise after the fit check.** Type II grows about 5 µm per side. Mask the fits (the drawing lists them), or
  chase the tapped holes afterwards.
- **Stator bond.** The slip fit lets the stator sit up to 0.035 off centre before the adhesive cures. Centre it
  during the cure: shims in the air gap with the rotor fitted, or a mandrel off the Ø60 seat.

## 4. Printing the gears

Print from `cnc/step/sun.step`, `planet.step` and `ring_gear.step`. The STEP teeth are nominal (no backlash).

| | Do | Why |
|---|---|---|
| Process | Resin (SLA/DLP) or MJF/SLS nylon. Not 0.4 mm FDM | m1 teeth are 1.57 mm thick at the pitch circle, with 0.38 mm root fillets |
| Backlash | Slicer XY size / contour compensation **−0.07 to −0.09 mm** per side. That thins every outside contour (sun and planet teeth) and opens every inside contour (the ring's tooth spaces, the sun's bore) | Printer accuracy (±0.05 or worse) is coarser than the steel's 0.05–0.10 mm backlash. Nominal teeth will jam |
| Check each print | Span over 3 teeth on the sun: aim for **7.45–7.49** (nominal 7.632). Over 4 teeth on a planet: **10.53–10.57** (nominal 10.711). Calipers are fine | 0.07–0.09 per flank of thinning, both flanks counted in the span |
| Face width | Sand or print the gears to **11.8** | Only 0.5 mm of end clearance each side between the carrier plates |
| Planets | **Don't press the HK0609 cups into plastic.** Print a sleeve Ø10 × Ø6.1 × 11.8 and glue it into each planet's bore, then run the planets straight on the 6 mm pins with grease | A drawn cup takes its shape from its bore; plastic won't round it |
| Ring gear | **Don't press it into the flange.** With the compensation its OD comes out about Ø85.85: glue it against the lip with a dab of CA, or pin it | Ø86 s6 is 0.04–0.09 interference: plastic cracks or creeps, and squeezed teeth aren't true |
| Sun | The compensation opens the double-D to about Ø12.15 / 10.95 across the flats. It should slide onto the shaft's flats | |

Planet spacing: (72 + 18) / 3 = 30, a whole number, so three planets at 120° all mesh. Turn the output slowly as the
ring goes on.

## 5. What to check in the fit check

1. The carrier with its bearing drops into the Ø60 seat, and the clamp ring into the Ø90 counterbore, by hand.
2. Clamp-ring stack: measure B, d and R (`ASSEMBLY.md` section 3, step 3) and work out the clamp ring's height.
3. The flange goes on with the ring meshing, and the centring step (`ASSEMBLY.md` section 3, step 6) works.
4. The output turns 5 full turns by hand with no tight spot, with the motor's shaft (or a Ø12 dowel) in the sun.
5. No rubbing: sun and planets against the carrier plates, carrier against the clamp ring (1 mm), flange lip
   against the carrier disk.
6. The teardown order in STEVE (`teardown` animation) works in real life, both ways.

Write down every measurement. They tell you whether to order the steel gears as drawn.
