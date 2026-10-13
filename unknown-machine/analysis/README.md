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
Output bearing 61806 static: P0 150 N vs C0 2900 N (s0 19); tilting moment 3.45 N·m on one deep-groove row
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

### Gear material change (after this analysis)

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

These are idealised estimates for a speculative concept, not a certification. Nothing here makes the design
safe for real-world use. See the repository license (MIT, no warranty).
