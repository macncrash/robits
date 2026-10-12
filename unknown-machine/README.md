# Unknown machine: planetary joint actuator

![Reference image](images/reference.png)

An AI image generator produced this "machine" with no stated purpose. The project reads its outside features
as a design intent, then fills in the parts that would have to be inside for it to work. Our conclusion is
that it's a **robot-joint actuator**: a frameless brushless motor driving a single-stage planetary gearbox,
with a hollow shaft for cables, an encoder on the back, and a quick-release clamp that holds it on a
pedestal mount. Similar renders in the same series show robot arms, so this is most likely one of an arm's
joint modules shown standing on its own.

| Assembled | Inside (housing, flange and ring gear hidden) |
|---|---|
| ![Assembled](images/assembled-isometric.png) | ![Internals](images/internals-isometric.png) |

## Reading the image

| In the image | Interpreted as | Modelled |
|---|---|---|
| Finned middle section | Motor housing with cooling fins | 12-slot stator, copper windings, 14-pole surface-magnet rotor |
| Fine-toothed ring around the front disk | Fixed **ring gear** of a planetary stage | Sun 18 T, 3 planets 27 T, ring 72 T, module 1: **5:1 reduction** |
| Silver disk + small hub with a bore | Planet carrier = output, with a hollow cable pass-through | Two-plate carrier joined by 3 bridge posts, 3 pressed-in planet pins, 8 mm bore end to end |
| Knurled rear cap | Encoder cover | Code disk on the shaft + read head on the end bell |
| Bolted front flange | Retains the ring gear | 4 × M5×25 socket head screws into tapped holes in the housing |
| Top lever + silver band | Quick-release cam clamp | Band around the housing, lever pivoting on a pin |
| Base with 4 holes, side port | Mounting pedestal with cable exit | Saddle block + base plate with four Ø9 holes |

## Main numbers

- Envelope about 130 × 162 × 137 mm (flange Ø120 mm, motor can Ø96–112 mm)
- Gear ratio 1 + 72/18 = **5:1**; planets evenly spaced ((18 + 72) is divisible by 3) and phased to mesh
- Bearings: 61806 (30 × 42 × 7) carries the output, 6001-2RS (12 × 28 × 8) at the rear, HK1210 needle
  bearing pilots the shaft's front end inside the carrier
- Through-bore: 8 mm from the rear cap to the output hub

## Parts list

Bought-in parts use real catalogue STEP models where an exact match exists. They come from
[step.parts](https://www.step.parts), an open-source (MIT) catalogue. The rest are modelled at catalogue
dimensions.

| Qty | Part | Material (modelled) | Source |
|---|---|---|---|
| 1 | Motor housing | 6061-T6 aluminium, anodised | made |
| 1 | Rear end bell | 6061-T6 aluminium, anodised | made |
| 1 | Encoder cap (knurled) | 6061-T6 aluminium, anodised | made |
| 1 | Encoder disk | 304 stainless | made |
| 1 | Encoder read head | PC | bought (placeholder shape) |
| 1 | Rear bearing **6001-2RS** (12 × 28 × 8) | bearing steel (C60 stand-in) | **catalogue STEP**: [step.parts `bearing_6001_2rs_sealed_simple`](https://www.step.parts/parts/bearing_6001_2rs_sealed_simple) |
| 1 | Stator core | steel (lamination stack stand-in) | bought with the motor |
| 1 | Windings | C10200 copper | bought with the motor |
| 1 | Rotor + hollow shaft + magnets | steel (magnets: NdFeB, steel stand-in) | bought with the motor |
| 1 | Sun gear, m1 18T | steel (see analysis: needs case hardening) | made |
| 3 | Planet gear, m1 27T | steel (see analysis) | made |
| 1 | Ring gear, m1 72T internal | steel | made |
| 1 | Planet carrier (output) | 304 stainless | made |
| 3 | Planet pin, dowel **ISO 2338 6 m6 × 18** | hardened steel | bought, modelled at catalogue size* |
| 1 | Pilot needle bearing **HK1210** (12 × 16 × 10) | bearing steel | bought, modelled at catalogue size* |
| 1 | Output bearing **61806** (30 × 42 × 7) | bearing steel | bought, modelled at catalogue size* |
| 1 | Front flange | 6061-T6 aluminium, anodised | made |
| 4 | Socket head cap screw **ISO 4762 M5 × 25** | A2-70 stainless | **catalogue STEP**: [step.parts `iso4762_socket_head_cap_screw_m5x25`](https://www.step.parts/parts/iso4762_socket_head_cap_screw_m5x25) |
| 1 | Clamp band | 304 stainless | made |
| 1 | Clamp lever | 6061-T6 aluminium, anodised | made |
| 1 | Pedestal | 6061-T6 aluminium, anodised | made |

\* No exact catalogue model was available, so these are modelled at the standard's dimensions:

- **61806 and HK1210:** step.parts has neither part.
- **ISO 2338 dowel pins:** step.parts lists them, but its files are twice their nominal length (its "6 × 16"
  measures 32 mm), so they weren't used.
- **Gears:** the catalogue only has small module 0.5 gears, 4 mm wide. Nothing matches module 1 / 12 mm
  wide, and internal ring gears are rarely sold off the shelf.

Swapping in the catalogue parts also changed the carrier. With separate pressed-in pins, nothing joined its
two plates any more, so it gained three bridge posts between the planets (2 mm clear of the planet tips).

## Files

```
images/
  reference.png              the AI-generated image this started from
  assembled-isometric.png    render of the model
  internals-isometric.png    render with the outer parts hidden
source/                      CadQuery source for the STEVE CAD design
  main.py                    places the parts, joints, gear coupling, teardown animation, fit check
  params.py                  gear module and tooth counts
  assembly_data.py           teardown order, flange screw pattern
  gearing.py                 involute spur and internal gear profiles
  shapes.py                  small geometry helpers (rings, boxes, ball bearings)
  components/*.py            one file per part (catalogue parts import their step.parts STEP by sha256)
  parts/carrier.py           planet carrier, a separate part linked into the design (`from links import carrier`)
  parts/pedestal.py          pedestal, likewise
analysis/
  README.md                  stress / strain results (FEA and hand calculations) and what they mean
  hand_calcs.py              gear, pin, bolt and bearing checks; plain Python 3
exports/
  step/unknown-machine-assembly.step   full assembly, every part in place
  step/components/*.step               one STEP per part
  stl/*.stl                            one STL mesh per part, mm, made from the STEP files
```

Part files sit at their assembled position, except `planet`, `planet_pin`, `flange_screw` and `rear_bearing`.
Those are modelled at their own origin and placed by `source/main.py` (3×, 3×, 4× and 1×).

There are no DXF files because nothing in this design is sheet metal or laser-cut flat stock.

### Motion in the source

- `spin`: the motor turns the sun, planets and carrier at the correct planetary ratios.
- `teardown` animation (about 14 s): takes the unit apart in a service order. The lever opens, then the
  screws, flange, carrier with planets, ring gear and output bearing come out of the front. The band, encoder
  cap, encoder disk and end bell with its bearing come off the back, then the rotor and stator come out and
  the unit lifts off the pedestal.
- `exploded` pose: every part pulled apart along the axis.
- A fit check (interference between all 378 part pairs, with declared seats, gear meshes and screw threads)
  passes on this revision.

Frame: the motor axis is +Z with the output at +Z, and the pedestal points toward −Y.

## Stress and strain

Summary of [analysis/README.md](analysis/README.md), at an assumed 20 N·m peak output torque:

- **Planet carrier:** peak 12.5 MPa, 0.37 µm deflection, about 65 µε strain, roughly 17× below yield.
  Under a 150 N overhung arm load it deflects 5.3 µm.
- **Pedestal:** 0.84 MPa peak, so it is heavily oversized.
- **Gear teeth:** bending is fine at 67 MPa. Contact stress at the sun is **657 MPa**, so the gears need case
  hardening.
- **Planet pins:** bending is fine. The plain planet journals run too hot (PV 2.4 MPa·m/s at 3000 rpm)
  without needle bearings.
- **Flange screws:** hold 7.5× the ring-gear reaction by friction.

## Caveats

- This is an **interpretation**, not a reconstruction. The image doesn't fully commit to any one mechanism.
  A strain-wave (harmonic) drive fits about as well as the planetary stage chosen here. The planetary
  version was chosen because its ring-gear teeth show around the output disk, as in the image.
- The rear bearing and the flange screws are catalogue CAD models. The other bought parts are simplified
  shapes at catalogue dimensions, and the magnets are a steel stand-in.
- Gears have zero backlash. The motor torque behind the [stress analysis](analysis/README.md) is assumed,
  not taken from a datasheet.
- The analysis found weak points worth fixing in a real build: gear contact stress needs case-hardened
  gears, the planets need needle bearings, and the output wants a crossed-roller bearing.
- Provided under the repository's [MIT license](../LICENSE), without warranty of any kind.
