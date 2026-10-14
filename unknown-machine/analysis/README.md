# Stress and strain analysis

These are first-pass strength checks of the interpreted actuator. Two kinds were used:

- **FEA (STEVE):** linear-elastic stress, steady heat, thermal stress and natural-frequency studies, run
  in STEVE (CalculiX solver, quadratic tetrahedra), one part at a time.
- **Hand calculations:** standard formulas, used as a cross-check on the FEA and for what single-part FEA
  without contact can't capture: gear contact (Hertz) stress, journal heating, bolted-joint friction and
  bearing ratings. They are in [`hand_calcs.py`](hand_calcs.py), which runs on plain
  Python 3 with no dependencies.

There's no motor datasheet for an imagined machine, so the load case is assumed:

| Input | Value | Why |
|---|---|---|
| Peak motor torque | 4 N·m | Typical for a frameless BLDC motor of about 85 mm with a stack of about 35 mm |
| Output torque | 20 N·m | 4 N·m × the 5:1 planetary ratio (losses ignored, so slightly conservative) |
| Ring-gear reaction | 16 N·m | Output torque − input torque |
| Motor speed | 3000 rpm | Used only for the gear dynamic factor and the planet-pin sliding speed |
| Planet load sharing | 1.15 | Tolerances mean the 3 planets don't share the load exactly equally |
| Arm load on the output | 150 N radial + 100 N axial | Assumes a small arm link with a payload on the output face |

Everything is linear, so results scale directly with torque. Change the inputs at the top of
`hand_calcs.py` and run it again.

## FEA results (all solved in STEVE)

Every study below was solved in STEVE. All runs pass the solver's own checks: force and moment balance (static),
energy balance (thermal) and orthogonality (modal), each with residuals around 1e-8 relative or better.

STEVE solves one solid per study, and its face names aren't available on the full assembly. So each studied
part is its own STEVE part, rebuilt with the same dimensions as the assembly's part. The carrier and pedestal
are also linked back into the design. The whole gears are too large to mesh finely enough within STEVE's 6 GB
solve limit. Gear teeth are therefore studied on a 3-tooth slice, linked to the full gear part. The slice is
held at its bore (or outer diameter, for the ring) and at its two cut faces, and the middle tooth is loaded at
its tip. That is the worst case, and the one the Lewis formula assumes.

### Stress and deflection

| Part / load case | Peak von Mises | Max displacement | Yield (material) | Factor on peak |
|---|---|---|---|---|
| Planet carrier, 20 N·m output torque<br>(pin holes held, torque through the six M4 output holes) | 12.5 MPa (1.5 mm mesh; 13.2 MPa at the default mesh) | 0.37 µm | 215 MPa (304 stainless) | ≈ 17 |
| Planet carrier, overhung arm load<br>(held at the 61806 seat, load on the front face) | 11.0 → 17.9 → 22.8 MPa at 3.8 / 1.5 / 1.0 mm mesh (still rising, see below) | 5.3 µm (converged) | 215 MPa | ≥ 9 |
| Pedestal, actuator weight + arm load + torque reaction, self-weight included<br>(base bolted down) | 0.84 MPa | 0.57 µm | 276 MPa (6061-T6) | > 300 |
| **Sun tooth**, 248 N tip load (Ft 170 N × dynamic factor 1.46), 0.38 mm root fillet | 129 → 143 MPa at 0.4 / 0.25 mm mesh | 2.2 µm | 235 MPa (S235, as modelled) | ≈ 1.6 |
| Sun tooth, same load, sharp root (as first modelled) | 133 → 159 MPa at 0.4 / 0.25 mm (singular) | 2.5 µm | 235 MPa | — |
| **Planet tooth**, 248 N tip load, 0.38 mm root fillet | 109 MPa (0.4 mm; 125 MPa with a sharp root) | 1.9 µm | 235 MPa | ≈ 2.2 |
| **Ring tooth**, 248 N tip load, 0.38 mm root fillet, held at its OD | 68 MPa (0.4 mm) | 1.4 µm | 235 MPa | ≈ 3.5 |
| **Planet pin** (ISO 2338 6×18), 341 N from the planet over its 12 mm journal; both press fits held | 47 → 55 MPa at 0.6 / 0.3 mm mesh (peak at the edge of the press fit) | 0.55 µm | ≈ 1100 MPa (hardened dowel) | ≈ 20 |
| **Motor housing**: ring-gear reaction 16 N·m through the 4 tapped holes + 150 N radial / 100 N axial on the 61806 seat; held at the clamp-band zone | 3.6 MPa | 1.8 µm | 276 MPa (6061-T6) | > 75 |
| **Clamp lever**, 100 N hand push on the grip, closed (cam cheeks and pivot held) | 155 MPa | 0.50 mm | 276 MPa (6061-T6) | ≈ 1.8 |
| Clamp lever, same push, pivot pin alone held (pin takes the moment in torsion) | 144 MPa | 0.62 mm | 276 MPa | ≈ 1.9 |

Peak strain in the carrier at 20 N·m is about σ/E = 12.5 MPa / 193 GPa ≈ **65 µε**. At the sun tooth root it
is about 140 MPa / 210 GPa ≈ **670 µε**.

### Heat (motor losses)

| Study | Result |
|---|---|
| Housing, steady state: 40 W of motor losses into the stator bore, natural convection plus radiation on every outer face (h = 12 W/m²K), 25 °C air | **85–87 °C** everywhere on the housing. The energy balance closes: 40.0 W in, 40.0 W out by convection. |
| Same heat, as thermal stress: assembled at 25 °C, clamp-band zone held rigidly (an upper bound) | 211 MPa peak at the band edges, 0.14 mm thermal growth. A real stainless band grows too (17 vs 23.6 µm/m·K), so the true stress is a fraction of this. |

The 40 W is an assumption: roughly a 90 %-efficient motor delivering 400 W continuous. Temperatures rise in
proportion to the losses (85 °C ≈ 25 °C + 1.5 K per watt).

### Natural frequencies (modal)

| Part (support) | First mode |
|---|---|
| Planet carrier (held at the output-bearing seat) | 3.48 kHz |
| Motor housing, empty (held at the clamp-band zone) | 5.10 kHz |
| Pedestal alone (base bolted down) | 18.4 kHz |

For comparison, the excitations at 3000 rpm are: shaft 50 Hz, magnet pole-pass 350 Hz (7 pole pairs) and gear
mesh 720 Hz (72 ring teeth × 10 carrier rev/s). Every part's own first mode is far above all of them. These are
single parts without the masses they carry, though. The actuator (about 2 kg) sitting on the pedestal, or an arm
on the output, brings the real system frequencies far lower. STEVE can't add lumped masses to a modal study, so
the assembled system wasn't solved.

How to read these numbers:

- **Overhung-load peak (the carrier's second case).** The peak keeps rising as the mesh is refined, which
  marks a stress singularity at a sharp inside corner: where the bearing sleeve meets the rear plate. That
  corner has no fillet in the model. The displacement has converged. Adding a fillet there turns the peak into
  a real, finite number. The fillet can be at most about 0.5 mm before it reaches the 61806 inner ring. Even the
  unconverged 22.8 MPa is about 9× below yield.
- **Gear teeth.** The first gear models had sharp tooth-root corners. Those corners made the peak stress keep
  climbing with mesh refinement, so each gear part was given the standard hob root fillet of 0.38 × module. The
  filleted sun tooth still creeps up a little (129 → 143 MPa). The remaining creep comes from the load and
  support edges, not from the root. The FEA peak is about 2× the Lewis nominal of 67 MPa, which is the usual
  stress concentration at a gear root (Lewis leaves it out). Against the soft S235 used in the model, the sun has
  a factor of about 1.6 on yield, and the peak sits at or near S235's fatigue limit. The case-hardened gear
  steel that the contact stress already requires (below) fixes this too.
- **Planet pin.** The peak sits on the edge of the fixed press-fit zone, a support singularity, so it creeps up
  with refinement. The deflection has converged at 0.55 µm. It is about 20× below the yield of a hardened dowel.
- **Housing.** Mechanically it is lightly loaded. Its real limit is **heat**: 85 °C at the case means the
  windings run hotter, and standard NdFeB magnets (N grades) start losing strength above about 80 °C. Use
  high-temperature magnets (SH/UH grades), heat-sink the unit through the pedestal, add airflow or derate
  continuous torque.
- **Clamp lever.** The two 4 × 6 mm side bars that join the cam cheeks to the arm are its weak spot. A hand
  check gives 5.2 N·m / (2 × 4·6²/6 mm³) ≈ 108 MPa nominal, and the sharp corners raise that to 155 MPa. A firm
  100 N push is fine, but leaning on it hard (200 N or more) would bend it. Make the bars about 10 mm deep, or
  the lever steel.
- **Pedestal.** It is heavily oversized for these loads. It could be pocketed or made much thinner.
- **Idealised supports.** The supports are stiffer than the real parts: holes are fully fixed, and a bearing
  seat is treated as fixed. Contact, bolt preload, fatigue, press-fit stresses and gear contact (Hertz) stress
  are not modelled. STEVE studies one solid at a time with no contact, so tooth contact stress comes from the
  hand calculation below.

### STEVE parts used for the studies

| STEVE part | Studies |
|---|---|
| Planet carrier (output) | output torque, overhung load (+ mesh check), modal |
| Pedestal | combined load, modal |
| Sun / Planet / Ring gear (unknown machine), with 0.38 mm root fillets | source geometry for the tooth slices |
| Sun / Planet / Ring gear tooth sector (study model) | tooth bending (sharp and filleted, mesh checks) |
| Planet pin ISO 2338 6x18 (unknown machine) | pin bending (+ mesh check) |
| Motor housing (unknown machine) | torque + bearing load, steady heat, thermal stress, modal |
| Clamp lever (unknown machine) | hand push (two support cases) |

## Hand calculations

Output of `python3 hand_calcs.py`:

```
Ratio 5.0:1, output torque 20 N·m, ring reaction 16 N·m
Tooth force per mesh Ft = 170 N (K_share 1.15), v = 2.83 m/s, Kv = 1.46
Lewis bending: sun 67 MPa, planet 59 MPa
Hertz contact: sun-planet 657 MPa, planet-ring 328 MPa
Planet pin: load 341 N, bending 26 MPa, journal p 4.7 MPa, v 0.50 m/s, PV 2.38 MPa·m/s
Flange slip torque with A2-70 stainless screws: 120.0 N·m vs 16 N·m needed (x7.50)
Flange slip torque with 8.8 steel screws: 210.0 N·m vs 16 N·m needed (x13.12)
Flange slip torque with 12.9 steel screws: 315.0 N·m vs 16 N·m needed (x19.69)
M5 thread engagement in aluminium: 9.5 mm = 1.9 d (aim >= 2 d)
Carrier joint: 3 x M4 friction holds 25.3 N·m vs 23 N·m worst case (x1.10); planet pins as dowels: 12 MPa shear each
Motor: copper loss 33 W at 1.3 N·m duty, 83 W at the 2.06 N·m continuous rating; peak-current limit 5.9 A for 4.0 N·m
Housing on the pedestal in still air at 1.20 K/W (was 1.58 on the band): about 64 °C at the duty torque (copper only), 124 °C at the motor's full continuous rating
Pedestal screws: friction holds 134 N·m about the axis vs 20 N·m output reaction (x6.7), plus 2 dowels; 10.2 mm = 2.0 d of M5 thread
Bond shear at 4.0 N·m: stator 12 kPa (half the bore bonded), rotor 94 kPa vs about 30 MPa lap shear
Output bearing CRBH 3510: 150 N radial, 100 N axial, 3.45 N·m tilting moment; check the maker's moment rating (the old 61806: s0 19 on force alone)
```

## What this says about the design

| Item | Verdict | Action |
|---|---|---|
| Gear tooth bending | Marginal in S235, OK in gear steel | FEA peak 143 MPa at the sun root (Lewis nominal 67 MPa). That is a factor of about 1.6 on S235 yield and about at its fatigue limit. Case-hardened gear steel is needed anyway (next row). Model the gears with a root fillet, as the STEVE gear parts now have. |
| **Gear tooth contact (sun–planet)** | **Fails as modelled** | 657 MPa is above what the soft structural steel used in the model (S235) can take without pitting. It needs case-hardened gears (16MnCr5 / 20MnCr5, allowable ≈ 1300–1500 MPa). Through-hardened 42CrMo4 would be marginal. |
| Planet pins (ISO 2338 6×18, hardened) | OK in bending | FEA ≈ 50 MPa at the press-fit edge (hand calculation 26 MPa nominal), about 20× below yield |
| **Planet journals** | **Too hot for plain sliding** | PV 2.4 MPa·m/s at 3000 rpm continuous. Fit a drawn-cup needle bearing in each planet (6 mm bore, 10 mm OD; the planet has room for it), or limit continuous speed. |
| Flange screws (4 × M5) | OK | Friction holds 7.5× the ring reaction, even with stainless screws |
| M5 threads in the aluminium housing | Borderline | 1.9 d engagement. Use thread inserts or tap 2–3 mm deeper. |
| Output bearing 61806 | OK for force, weak for moment | A single thin deep-groove row has to carry the arm's tilting moment. A real robot joint would use a crossed-roller bearing here. |
| Carrier | OK | Peak stress factor ≥ 9. Add a fillet (up to about 0.5 mm, to clear the 61806 inner ring) at the sleeve-to-plate corner. |
| Pedestal | Heavily oversized | Can be lightened |
| **Motor heat** | **Hot** | About 85 °C on the case at an assumed 40 W of continuous losses in still air. Use high-temperature magnets, heat-sink through the pedestal, add airflow, or derate continuous torque. |
| Clamp lever | OK for normal use, weak if abused | Side bars reach 155 MPa at 100 N. Deepen them to about 10 mm, or make the lever steel. |
| Housing | OK | 3.6 MPa under the torque and bearing loads; first mode 5.1 kHz |
| Vibration | OK at part level | Every part's first mode is above 3.4 kHz, against a 720 Hz gear mesh. The assembled system on its pedestal wasn't solved. |

## Design changes after this analysis

### Gear material

The gears were moved off S235 as the verdicts above call for. The STEVE library has no 16MnCr5 / 20MnCr5,
so the nearest equivalent case-hardening steel was used:

| Gear | Was | Now | Why |
|---|---|---|---|
| Sun, 3 planets | S235JR | **17CrNiMo6 (18CrNiMo7-6)**, carburised to about 58–62 HRC | Carries the 657 MPa sun–planet contact; typical allowable about 1500 MPa, core yield about 800 MPa |
| Ring | S235JR | **34CrNiMo6**, quenched and tempered (nitriding optional) | Only 328 MPa contact and 68 MPa bending; internal rings are normally through-hardened or nitrided, not carburised |

The tooth-bending stresses in the table above don't change. They depend on geometry and load, and E is
practically the same for all these steels. Only the margins change: the 143 MPa sun peak is now about 5× below
core yield instead of 1.6×, and the contact stress is well inside the carburised allowable. These figures are
typical values; the supplier's data sheet and the heat treatment govern.

### Planet needle bearings

Each planet bore is now 10 mm and holds an HK0609 drawn-cup needle bearing (6 × 10 × 9) that runs directly on
the hardened ISO 2338 pin. That replaces the plain journal (PV 2.4 MPa·m/s). The rim under the planet's teeth
drops from 9.0 to 7.25 mm, still about 3× the 2.25 mm tooth height, so tooth bending is unaffected. Check the
needle bearing's rating against the 341 N planet load and about 1600 rpm relative speed on the chosen
catalogue part.

### Crossed-roller output bearing

The 61806 is replaced by a CRBH 3510 crossed-roller bearing (35 × 60 × 10), which takes the arm's radial,
axial and tilting loads in one row. The housing bulkhead grows to z 31–44 with a 60 mm seat; the carrier
sleeve grows from Ø30 to Ø35 and starts 3 mm further back. Check the static moment rating against the
3.45 N·m tilting moment from `hand_calcs.py` on the chosen part. The housing studies were re-run with
this bulkhead and the KBM motor bore; see [Motor](#motor) below.

### Clamp lever

The side bars and the arm are now 10 mm deep (were 6 mm). Same study as above, re-run in STEVE (100 N push on
the grip, cam cheeks and pivot held). The setup was first checked against the original lever, where it
reproduced 155.1 MPa against the earlier 154.8 MPa.

| Lever | Peak von Mises | Max displacement | Factor on 276 MPa yield | Mass |
|---|---|---|---|---|
| Original, 4 × 6 mm side bars | 155 MPa | 0.50 mm | 1.8 | 27.7 g |
| Side bars only 10 mm deep | 123 MPa | 0.37 mm | 2.2 | 28.3 g |
| **Side bars and arm 10 mm deep (adopted)** | **62 MPa** | **0.13 mm** | **4.5** | 42.2 g |

Deepening only the bars moved the peak to the step where they met the thinner arm. Making the arm flush
removed that step. A 200 N shove now reaches about 124 MPa, still 2.2× below yield.

### Two-piece carrier in 303

The one-piece carrier had to be milled sideways between its plates, through the three windows between the
posts, from Ø70 bar: about 80% of the bar became chips, in gummy 304. It is now two pieces:

- **Rear part:** sleeve, rear plate and three posts, milled from the open front face. Tapped M4 in each post.
- **Front disk + output hub:** turned, with three 90° countersinks. The disk is 5 mm thick (was 3) so the heads
  sit flush; the output face stays at z 72.
- **Joint:** 3 × ISO 10642 M4 × 12 (A2-70) into the posts, 7 mm of thread each. The three planet pins pass
  through both pieces and act as the dowels. Bore the pin holes with both pieces clamped together.
- **Material:** AISI 303 (1.4305), the free-machining grade. STEVE's library has no 303, so the model uses
  304, which has the same stiffness and density and a slightly lower yield (215 vs about 240 MPa annealed).

Each piece was studied in STEVE with the whole 20 N·m (341 N per planet pin, load sharing included) going
through it, which is conservative: in reality the pins share their load between the two plates.

| Piece and load path | Support | Peak von Mises | Max displacement | Factor on 215 MPa |
|---|---|---|---|---|
| Rear part: all pin load in the rear plate | Post tops and screw holes | 21.6 MPa | 1.4 µm | 10 |
| Front disk: all pin load in its pin holes | Six M4 load holes | 14.8 MPa | 0.29 µm | 15 |
| Front disk: all load through the three screws | Six M4 load holes | 16.2 MPa | 0.31 µm | 13 |

The joint itself (`hand_calcs.py`): three M4 screws at 2.5 kN preload hold 25 N·m by friction, 1.1× the
23 N·m worst case where all the torque crosses the joint. The pins back that up: carrying their planet's
341 N across the joint, each sees 12 MPa shear. The rear part's peak is at the sharp post-to-plate corner; a
1 mm fillet there would lower it.

### Motor

The motor is now a Kollmorgen KBM-17H01-B00 (155 °C winding rating, PTC thermistor), run from a 240 Vac drive.
See [Motor](../README.md#motor-kollmorgen-kbm-17h01-b00) in the project README. The housing's bore is now
Ø85.10 from the rear to a depth-stop ledge at z 29–31, so its walls are 0.55 mm thinner than before, and the
bulkhead is the thicker crossed-roller one. All four housing studies were re-run on that geometry in STEVE
(Motor housing part, revision 4), with the 40 W going in through the bore where the stator is bonded
(z −26 to 29) and the clamp band zone (z 20–32) as the support:

| Study | Before (61806 bulkhead, generic motor) | Now (CRBH 3510 bulkhead, KBM-17 bore) |
|---|---|---|
| Ring-gear reaction 16 N·m + 150 N radial / 100 N axial on the bearing seat | 3.6 MPa, 1.8 µm | **0.84 MPa, 0.44 µm** |
| Steady heat, 40 W, h = 12 W/m²K, 25 °C air | 85–87 °C | **87.8–88.5 °C** |
| Thermal stress, band zone held perfectly rigid (upper bound) | 211 MPa, 0.14 mm | 294 MPa, 0.13 mm |
| Thermal stress, rigid band that grows with the housing (304 band: only the 6.6 µm/m·K difference loads it) | — | **82 MPa, 0.036 mm** |
| First natural frequency, held at the band zone | 5.10 kHz | **4.83 kHz** |

All runs pass STEVE's balance checks (force and energy residuals around 1e-8 relative). How to read them:

- **Stress.** The thicker bulkhead carries the bearing and ring loads with almost nothing: under 1 MPa.
- **Thermal stress.** The 294 MPa rigid-band figure is above 6061-T6 yield, but no real band is rigid and
  fixed in size: it is stainless and heats up with the housing. The second case holds the band zone just as
  rigidly but subtracts the band's own growth. 82 MPa is still an upper bound, because a real band also
  stretches. That is about 3.3× below 6061-T6 yield at 88 °C (about 270 MPa). Peak stress is at the edges of
  the band zone. Don't over-tighten the clamp: preload adds to this.
- **Heat.** The housing rises about 1.58 K per watt in still air, so 40 W gives about 88 °C. From the KBM
  catalog, the copper loss is 1.5 × I² × Rm: about 33 W at the 1.3 N·m duty torque. With iron losses at
  3000 rpm, 40 W is a fair estimate. The winding is rated 155 °C, so the case leaves about 65 K for the
  winding-to-case rise. The PTC thermistor should trip the drive before that runs out.
- **Continuous torque is limited by the housing, not the motor.** At the motor's own 2.06 N·m continuous
  rating, copper loss alone is about 83 W, which would put this housing at about 156 °C in still air. In
  this package, without a heat path through the pedestal or airflow, plan on about 1.3–1.5 N·m continuous
  motor torque (6.5–7.5 N·m at the output). Full 4 N·m peaks are fine for short bursts. *(Superseded: with the
  housing bolted into the pedestal, see the next section.)*
- **Bonds.** At 4 N·m, the stator bond sees about 12 kPa of shear (with only half the bore bonded) and the
  rotor bond about 94 kPa. Both are hundreds of times below the about 30 MPa lap shear of Scotchweld 2214.
  The bond's real limits are temperature and cure, not strength: stay under the adhesive's rated temperature,
  and follow Kollmorgen's 82 °C limit for curing the rotor outside the stator.
- **Not yet modelled.** The stator and rotor geometry still uses estimated bore and OD values until
  Kollmorgen's STEP model replaces them. The housing studies don't depend on those values; the stator OD and
  length are catalog values.

### Pedestal mount (clamp removed)

The clamp band and lever were removed. The housing now sits straight in a pedestal saddle bored to its
diameters, on a thermal pad. It is held by 4 × M5 × 20 screws from below and located by 2 × 4 mm dowels (see
[Pedestal mount](../README.md#pedestal-mount)). The thermal-stress results above no longer apply: aluminium
bolted to aluminium has no expansion mismatch at the joint.

STEVE parts: Motor housing rev 5 (with the mount holes), Pedestal rev 4. There is also a new study model,
"Housing on pedestal (study model)". It links both parts and fuses them into one solid, which treats the
saddle joint as perfectly bonded. That is a fair model for small vibrations and for heat through a pad held
closed by about 16 kN of screw preload. It is an upper bound on how much heat and stiffness the joint passes.

| Study | Setup | Result |
|---|---|---|
| Housing stress | Ring reaction 16 N·m + 150 N radial / 100 N axial on the bearing seat; held by the 4 tapped holes alone (saddle contact left out) | 9.8 MPa, 8.6 µm; peak at the held holes, about 28× below yield |
| Housing modal | Held by the 4 tapped holes alone | 903 Hz: the housing rocks on the two screw rows, which are only 10 mm apart. A lower bound: the saddle is ignored |
| Housing on pedestal, modal | Saddle bonded, base face fixed, original 44 mm saddle block | 1.33 kHz |
| Housing on pedestal, modal | Same, saddle block lengthened to z −20 (under the fins) | **1.82 kHz** |
| Housing on pedestal, heat | 40 W into the stator bore, h = 12 W/m²K on the outside, base insulated | **69–73 °C** (1.20 K/W, was 1.58 K/W on the band) |
| Housing on pedestal, heat | Same, base held at 35 °C (bolted to a metal structure) | **35–44 °C**; 28 W of the 40 W go out through the base |

All runs pass the balance checks. Meshing notes: the default 7 mm quadratic mesh failed its high-order pass
around the small tapped holes. The stress study ran at 3 mm. The modal studies ran at 4 mm with
`high_order_optimization: optimization`. The face list STEVE returns is cut off after the 60 largest faces, so
convection was applied to those outer faces only. That leaves out some small faces, so the temperatures are
slightly high (conservative).

What it means:

- **Heat.** Continuous torque is now limited by the motor rather than the housing, as long as the pedestal is
  bolted to metal. With the base held at 35 °C, the housing runs at about 35 + 0.23 K/W × P. At the KBM's full
  2.06 N·m continuous rating (83 W copper loss) that is about 55 °C. On an insulating base it is
  25 + 1.20 × P, about 124 °C at 83 W, so derate there or add airflow.
- **Vibration.** The 1.82 kHz system mode has no motor, gears or bearings in it. Scaling by mass, those parts
  (about 1.5 kg) on the 0.64 kg housing would bring it to roughly 1 kHz. That's a rough estimate, but it is
  still above the 720 Hz gear mesh at 3000 rpm. Lengthening the saddle block raised the mode by 37%. If the
  measured mode turns out close to the mesh frequency, spread the screw rows further apart along the axis
  next. The side cable port, at z 10–24, currently stops the rear row from moving back.
- **Screws.** Friction alone holds 134 N·m about the axis (`hand_calcs.py`) against 20 N·m of output reaction.
  Each screw has 10 mm (2 d) of thread.

These are idealised estimates for a speculative concept, not a certification. Nothing here makes the design
safe for real-world use. See the repository license (MIT, no warranty).
