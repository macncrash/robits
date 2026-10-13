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
| Silver disk + small hub with a bore | Planet carrier = output, with a hollow cable pass-through | Two-piece carrier: rear part with 3 bridge posts + bolted front disk and hub, 3 pressed-in planet pins, 8 mm bore end to end |
| Knurled rear cap | Encoder cover | Code disk on the shaft + read head on the end bell |
| Bolted front flange | Retains the ring gear | 4 × M5×25 socket head screws into tapped holes in the housing |
| Top lever + silver band | Quick-release cam clamp | Band around the housing, lever pivoting on a pin |
| Base with 4 holes, side port | Mounting pedestal with cable exit | Saddle block + base plate with four Ø9 holes |

## Main numbers

- Envelope about 130 × 162 × 137 mm (flange Ø120 mm, motor can Ø96–112 mm)
- Gear ratio 1 + 72/18 = **5:1**; planets evenly spaced ((18 + 72) is divisible by 3) and phased to mesh
- Bearings: a CRBH 3510 crossed-roller bearing (35 × 60 × 10) carries the output and the arm's tilting
  moment; 6001-2RS (12 × 28 × 8) at the rear; HK1210 needle bearing pilots the shaft's front end inside the
  carrier; each planet runs on an HK0609 needle bearing (6 × 10 × 9)
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
| 1 | Windings | C10200 copper, class H (180 °C) insulation | bought with the motor |
| 1 | Rotor + hollow shaft + magnets | steel (magnets: NdFeB grade SH or UH, steel stand-in) | bought with the motor |
| 1 | Sun gear, m1 18T | 18CrNiMo7-6 (17CrNiMo6) case-hardening steel, carburised | made |
| 3 | Planet gear, m1 27T | 18CrNiMo7-6 (17CrNiMo6) case-hardening steel, carburised | made |
| 1 | Ring gear, m1 72T internal | 34CrNiMo6, quenched and tempered (nitriding optional) | made |
| 1 | Planet carrier, rear part (sleeve, rear plate, 3 posts) | 303 stainless (304 stand-in in the model) | made |
| 1 | Planet carrier, front disk + output hub | 303 stainless (304 stand-in in the model) | made |
| 3 | Countersunk socket screw **ISO 10642 M4 × 12** (front disk to posts) | A2-70 stainless | **catalogue STEP**: [step.parts `countersunk_socket_screw_m4_l0012_simple`](https://www.step.parts/parts/countersunk_socket_screw_m4_l0012_simple) |
| 3 | Planet pin, dowel **ISO 2338 6 m6 × 18** | hardened steel | bought, modelled at catalogue size* |
| 3 | Planet needle bearing **HK0609** (6 × 10 × 9), drawn cup | bearing steel | bought, modelled at catalogue size* |
| 1 | Pilot needle bearing **HK1210** (12 × 16 × 10) | bearing steel | bought, modelled at catalogue size* |
| 1 | Output bearing **CRBH 3510** crossed roller (35 × 60 × 10) | bearing steel | bought, modelled at catalogue size* |
| 1 | Front flange | 6061-T6 aluminium, anodised | made |
| 4 | Socket head cap screw **ISO 4762 M5 × 25** | A2-70 stainless | **catalogue STEP**: [step.parts `iso4762_socket_head_cap_screw_m5x25`](https://www.step.parts/parts/iso4762_socket_head_cap_screw_m5x25) |
| 1 | Clamp band | 304 stainless | made |
| 1 | Clamp lever (10 mm deep side bars and arm) | 6061-T6 aluminium, anodised | made |
| 1 | Pedestal | 6061-T6 aluminium, anodised | made |

\* No exact catalogue model was available, so these are modelled at the standard's dimensions:

- **CRBH 3510, HK0609 and HK1210:** step.parts has none of these. The crossed-roller bearing is a simplified
  model (two rings and 28 crossed rollers); check the final choice against the maker's drawing.
- **ISO 2338 dowel pins:** step.parts lists them, but its files are twice their nominal length (its "6 × 16"
  measures 32 mm), so they weren't used.
- **Gears:** the catalogue only has small module 0.5 gears, 4 mm wide. Nothing matches module 1 / 12 mm
  wide, and internal ring gears are rarely sold off the shelf.

Swapping in the catalogue parts also changed the carrier. With separate pressed-in pins, nothing joined its
two plates any more, so it gained three bridge posts between the planets (2 mm clear of the planet tips).
It is now made as two pieces, the rear part with the posts and a bolted front disk, so it can be machined from
the open front face; see [the analysis](analysis/README.md#two-piece-carrier-in-303).

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
  parts/carrier.py           planet carrier rear part, a separate part linked into the design (`from links import carrier`)
  parts/carrier_disk.py      planet carrier front disk and output hub, likewise (`from links import carrier_disk`)
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

Summary of [analysis/README.md](analysis/README.md), at an assumed 20 N·m peak output torque. Everything
below was solved in STEVE.

- **Planet carrier:** now two pieces (rear part + bolted front disk). At 20 N·m, with each piece taking the
  whole load in turn, the peaks are 21.6 MPa (rear part) and 16.2 MPa (front disk), at least 10× below yield.
  The one-piece carrier peaked at 12.5 MPa, 0.37 µm deflection, about 65 µε strain.
  Under a 150 N overhung arm load it deflects 5.3 µm.
- **Gear teeth (bending):** the sun tooth root reaches 143 MPa (planet 109, ring 68). That is a factor of
  about 1.6 on the soft S235 used in the model, so the gears need gear steel. Contact stress at the sun
  (657 MPa, from the hand calculation) says the same: **case-hardened gears**.
- **Planet pins:** about 50 MPa, roughly 20× below yield. Plain planet journals would run too hot (PV
  2.4 MPa·m/s at 3000 rpm), so each planet now runs on an HK0609 needle bearing.
- **Motor housing:** 3.6 MPa under the torque and bearing loads. Thermally, though, it reaches **about
  85 °C** at an assumed 40 W of continuous losses in still air, above what standard NdFeB magnets tolerate.
- **Clamp lever:** 155 MPa at a 100 N push with the original 6 mm deep side bars. With the bars and arm
  10 mm deep it is **62 MPa** and 0.13 mm (was 0.50 mm), about 4.5× below yield.
- **Pedestal:** 0.84 MPa peak, so it is heavily oversized.
- **Vibration:** every part's first natural frequency is above 3.4 kHz, against a 720 Hz gear-mesh
  frequency at 3000 rpm.
- **Flange screws:** hold 7.5× the ring-gear reaction by friction (hand calculation).

## Motor specification

The motor is a frameless BLDC kit (stator + rotor) pressed into the housing. The model's stator and rotor are
generic stand-ins, so the motor is specified by requirements rather than a part number:

| Requirement | Value | Why |
|---|---|---|
| Envelope | Stator OD ≤ 84 mm, stator ID about 56 mm, stack ≤ 36 mm | Fits the current housing bore and length |
| Topology | 12 slots / 14 poles (or similar concentrated winding) | As modelled; short end turns |
| Peak torque | ≥ 4 N·m | Gives 20 N·m at the output through the 5:1 stage |
| Continuous | ≥ 1.3 N·m at 3000 rpm (about 400 W) | The duty behind the 40 W loss / 85 °C case estimate |
| Magnets | Sintered NdFeB, grade **SH (150 °C) minimum, UH (180 °C) preferred** | The case reaches about 85 °C, so the rotor runs hotter; standard N grades start losing strength above about 80 °C |
| Winding insulation | Class H (180 °C) | Margin over the hot-spot temperature |
| Temperature sensor | PT1000 or KTY84 in the end turns | Lets the drive derate before the magnets are at risk |
| Supply | 48 V DC bus | Typical for robot joints of this size |

Frameless kits around this size to evaluate include the TQ RoboDrive ILM 85 and Kollmorgen KBM families. Their
dimensions, magnet grades and ratings haven't been checked here; confirm them against the datasheets, and
resize the stator and rotor parts to the chosen kit.

## Caveats

- This is an **interpretation**, not a reconstruction. The image doesn't fully commit to any one mechanism.
  A strain-wave (harmonic) drive fits about as well as the planetary stage chosen here. The planetary
  version was chosen because its ring-gear teeth show around the output disk, as in the image.
- The rear bearing and the flange screws are catalogue CAD models. The other bought parts are simplified
  shapes at catalogue dimensions, and the magnets are a steel stand-in.
- Gears have zero backlash. The motor torque behind the [stress analysis](analysis/README.md) is assumed,
  not taken from a datasheet.
- The analysis found weak points that have since been fixed in the model: case-hardened gear steel, planet
  needle bearings, a crossed-roller output bearing, a deeper lever and a high-temperature motor spec (see
  [Motor specification](#motor-specification)). Still open: a fillet at the carrier's sleeve-to-plate corner,
  2–3 mm deeper M5 threads (or inserts) in the housing, and a heat path out through the pedestal.
- The STEVE assembly (design revision 24) builds and passes its fit check (595 part pairs) with all these
  changes. The STEP and STL files in `exports/` haven't been regenerated yet and still show the revision 18
  geometry: re-export them from the STEVE model.
- The gears in the assembly source still have sharp tooth roots. The separate STEVE gear parts used for the
  stress studies add the standard 0.38 mm root fillet.
- Provided under the repository's [MIT license](../LICENSE), without warranty of any kind.
