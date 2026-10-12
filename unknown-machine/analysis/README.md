# Stress and strain analysis

These are first-pass strength checks of the interpreted actuator. Two kinds were used:

- **FEA:** linear-elastic finite-element studies, run in STEVE (CalculiX solver, quadratic tetrahedra), on
  single parts.
- **Hand calculations:** standard formulas for the parts that FEA without contact can't capture: gear
  teeth, pins, bolted joints and bearings. They are in [`hand_calcs.py`](hand_calcs.py), which runs on plain
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

## FEA results

| Part / load case | Peak von Mises | Max displacement | Yield (material) | Factor |
|---|---|---|---|---|
| Planet carrier, 20 N·m output torque<br>(pin holes held, torque through the six M4 output holes) | 12.5 MPa (1.5 mm mesh; 13.2 MPa at the default mesh) | 0.37 µm | 215 MPa (304 stainless) | ≈ 17 |
| Planet carrier, overhung arm load<br>(held at the 61806 seat, load on the front face) | 11.0 → 17.9 → 22.8 MPa at 3.8 / 1.5 / 1.0 mm mesh (still rising, see below) | 5.3 µm (converged) | 215 MPa | ≥ 9 |
| Pedestal, actuator weight + arm load + torque reaction, self-weight included<br>(base bolted down) | 0.84 MPa | 0.57 µm | 276 MPa (6061-T6) | > 300 |

Peak strain in the carrier at 20 N·m is about σ/E = 12.5 MPa / 193 GPa ≈ **65 µε**.

All runs pass the solver's force and moment balance checks, with residuals around 1e-8 relative.

How to read these numbers:

- **Overhung-load peak (the carrier's second case).** The peak keeps rising as the mesh is refined, which
  marks a stress singularity at a sharp inside corner: where the bearing sleeve meets the rear plate. That
  corner has no fillet in the model. The displacement has converged. Adding a 1 mm fillet at that corner
  turns the peak into a real, finite number. Even the unconverged 22.8 MPa is about 9× below yield.
- **Pedestal.** It is heavily oversized for these loads. It could be pocketed or made much thinner.
- **Idealised supports.** The supports are stiffer than the real parts: holes are fully fixed, and a
  bearing seat is treated as fixed. Contact, bolt preload, fatigue and press-fit stresses are not modelled.

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
| Gear tooth bending | OK | 67 MPa is well within reach of any gear steel |
| **Gear tooth contact (sun–planet)** | **Fails as modelled** | 657 MPa is above what the soft structural steel used in the model (S235) can take without pitting. It needs case-hardened gears (16MnCr5 / 20MnCr5, allowable ≈ 1300–1500 MPa). Through-hardened 42CrMo4 would be marginal. |
| Planet pins (ISO 2338 6×18, hardened) | OK in bending | 26 MPa |
| **Planet journals** | **Too hot for plain sliding** | PV 2.4 MPa·m/s at 3000 rpm continuous. Fit a drawn-cup needle bearing in each planet (6 mm bore, 10 mm OD; the planet has room for it), or limit continuous speed. |
| Flange screws (4 × M5) | OK | Friction holds 7.5× the ring reaction, even with stainless screws |
| M5 threads in the aluminium housing | Borderline | 1.9 d engagement. Use thread inserts or tap 2–3 mm deeper. |
| Output bearing 61806 | OK for force, weak for moment | A single thin deep-groove row has to carry the arm's tilting moment. A real robot joint would use a crossed-roller bearing here. |
| Carrier | OK | Peak stress factor ≥ 9. Add a 1 mm fillet at the sleeve-to-plate corner. |
| Pedestal | Heavily oversized | Can be lightened |

These are idealised estimates for a speculative concept, not a certification. Nothing here makes the design
safe for real-world use. See the repository license (MIT, no warranty).
