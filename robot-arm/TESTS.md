# Robot arm: stress, vibration and fit tests

Every test here was run in STEVE (simulation studies and design checks) on the arm design, revision 5.
The studies live in the design's Simulate workspace and the checks in `source/steve/arm/checks.py`.

## Load case

Worst static pose for each link: the arm stretched out level, a **3 kg payload** at the gripper, and
1 g gravity. Each study solves one link as one solid (STEVE's simulation limit), so everything beyond the
link is applied as an equivalent end force. That force gives the same bending moment at the link's root
as the real distal masses do:

| Link | Carries (beyond the link) | Equivalent force |
|---|---|---|
| Upper arm | Forearm, J3–J6 actuators, wrist, gripper, payload: 13.6 kg at up to 0.56 m from the elbow | 253 N at the elbow, plus the link's own weight |
| Forearm | J4–J6 actuators, wrist, gripper, payload: 9.5 kg | 120 N at the wrist, plus own weight |
| Wrist 2 knuckle | J6, gripper, payload: 5.7 kg, wrist rolled 90° | 243 N on the J6 mount |

Supports are the face that bolts to the driving actuator's output, held fixed. Material is 6061-T6
(E 68.9 GPa, yield 276 MPa).

## Stress and deflection (static)

| Link | Mesh | Peak von Mises | Max deflection | Hand check | Margin to yield |
|---|---|---|---|---|---|
| Upper arm | 4 mm | 7.6 MPa | 0.081 mm | 3.7 MPa nominal, 0.065–0.07 mm | 36× |
| Upper arm | 3 mm | 9.7 MPa | 0.082 mm | (refinement check) | 28× |
| Forearm | 3.5 mm | 6.7 MPa | 0.038 mm | 3.0 MPa nominal | 41× |
| Wrist 2 knuckle | 3 mm | 0.95 MPa | 0.0002 mm | 0.5 MPa nominal | ≫ 100× |

- The solver's force and moment balance closed to better than 3 × 10⁻⁸ in every run.
- **Deflection is mesh-converged:** refining the upper arm from 4 mm to 3 mm changed it by 1 %.
- **Peak stress is not mesh-converged.** It sits at the sharp, unfilleted joint between tube and hub, and
  it rises as the mesh is refined (7.6 → 9.7 MPa). The nominal stress (3–4 MPa) is the meaningful
  number. A real part needs a fillet there.
- **The links are stiffness-limited, not strength-limited.** Even the worst peak is well over 25× below
  yield. The forearm's peak rose from 5.0 to 6.7 MPa after the revision 5 trim, which added new sharp
  edges.

## Vibration (modal)

| Part | Support | First natural frequency | Hand check |
|---|---|---|---|
| Upper arm, link alone | Shoulder face fixed | 488 Hz | 499 Hz (cantilever tube, 2 % apart) |

This is the bare link. With the distal 13.6 kg lumped at the elbow and the stiffness from the static run
(3.1 N/µm), the link's own contribution is about 76 Hz. In a real arm the gearboxes are much softer than
these tubes, so the system's first mode would be set by joint stiffness: typically 10–20 Hz for a cobot
of this size.

## Fit and interference

The fit check declares each actuator as seated on the two links it joins, and requires 1 mm clearance
everywhere else.

**Revision 4 found four real interferences, all fixed in revision 5:**

| Problem found | Size | Fix |
|---|---|---|
| Forearm tube poked into the J3 actuator (tube 80 mm wide, hub 70 mm) | 2,157 mm³ overlap | Tube trimmed flush with the hub faces near the elbow |
| J2 clamp lug (r 72.8 mm) cut into the turret cradle (r 72 mm) | 169 mm³ overlap | Cradle cut opened to r 75 mm |
| Wrist-2 neck ran into the J5 actuator's front flange | overlap at rest | Neck changed to a 30 × 60 mm block within the hub's length |
| J5 and J6 actuator housings touching | 0 mm (needs 1 mm) | J6 lowered 2 mm |

**Revision 5:** nothing overlaps at rest or at the `flourish` pose (136 instance pairs). The only finding
is a 0.06 mm³ contact between wrist 1 and J5 at `flourish`, a seated pair, which is numerical contact
rather than interference.

## Collisions across the range of motion

| Study | What it checks | Revision 4 | Revision 5 |
|---|---|---|---|
| `pick_and_place` animation check | 48 samples of the animation | clear (2 pairs overlapping at rest) | clear, nothing at rest |
| `pick_and_place_keys` | 12 key poses, near misses < 5 mm | 0 collisions | 0 collisions; closest 1–2 mm (designed gaps) |
| `shoulder_elbow` | J2 × J3 grid, 20° steps over the limits | 35 of 204 collide | 0 of 132 collide |
| `arm_pitch` | J2, J3, J4 random, 150 poses | 32 % collide | 9.3 % collide (95 % CI 5.6–15 %) |

- **Elbow (J3) limit.** It was ±160°. Between +40° and +130° the wrist folded into the shoulder actuator
  and upper arm, up to 65 mm deep. The limit is now **−160° to +30°**, and the J2 × J3 grid is clear
  across its whole range.
- **Wrist pitch (J4), what's left.** With J4 at about +90° to +130°, the gripper fingers reach back into
  the J3 actuator or the upper arm (up to 15.6 mm deep). That's a reach-back zone that depends on the
  pose, so a hard limit isn't the right fix. Real cobots handle this with a software keep-out zone, or
  J4 can be restricted to about −180° to +80° if that's acceptable.

## What these tests don't cover

- **Joint internals:** no gearbox, bearing, bolt or joint stiffness. The actuators are exterior shells.
- **Analysis types:** no fatigue, buckling, dynamic or impact loads, contact or plasticity. The loads
  are 1 g static; real accelerations add load roughly in proportion.
- **Not checked by simulation:** the cast base, the turret and the gripper. They are multi-body
  components, which STEVE's single-solid studies can't solve as modelled.
- **Not a certification.** These are idealised linear-elastic estimates.
