# Robot arm: stress, vibration and fit tests

Every test here was run in STEVE (simulation studies and design checks) on the arm design, revision 11.
The studies live in the design's Simulate workspace and the checks in `source/steve/arm/checks.py`.
Earlier revisions' numbers are kept where they show what a fix changed.

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

Revision 10 rounded the tube-to-hub seams: a 4 mm fillet on the upper arm and 3 mm on the forearm.

| Link | Geometry | Mesh | Peak von Mises | Max deflection | Hand check | Margin to yield |
|---|---|---|---|---|---|---|
| Upper arm | sharp seam (rev 5) | 4 mm | 7.6 MPa | 0.081 mm | 3.7 MPa nominal, 0.065–0.07 mm | 36× |
| Upper arm | sharp seam (rev 5) | 3 mm | 9.7 MPa | 0.082 mm | (refinement check) | 28× |
| **Upper arm** | **4 mm fillet (rev 10)** | 3 mm | **6.8 MPa** | **0.071 mm** | 3.7 MPa nominal, 0.065–0.07 mm | **41×** |
| Forearm | sharp seam (rev 5) | 3.5 mm | 6.7 MPa | 0.038 mm | 3.0 MPa nominal | 41× |
| **Forearm** | **3 mm fillet (rev 10)** | 2.5 mm | **10.3 MPa** | **0.038 mm** | 3.0 MPa nominal | **27×** |
| Wrist 2 knuckle | unchanged | 3 mm | 0.95 MPa | 0.0002 mm | 0.5 MPa nominal | ≫ 100× |

- The solver's force and moment balance closed to better than 1 × 10⁻⁸ in every run.
- **Upper arm: the fillet did what it should.** The sharp-seam peak kept rising as the mesh was refined
  (7.6 → 9.7 MPa), the mark of a stress singularity. With the 4 mm fillet the peak drops to 6.8 MPa and
  sits on the fillet's toe, about 1.8× the nominal bending stress, a normal concentration factor for a
  tube-to-hub joint. Deflection now matches the hand check.
- **Forearm: the fillet only partly took.** The forearm tube is 80 mm wide but its hub only 70 mm, so
  the tube is trimmed flat where it passes the J3 actuator. STEVE's kernel could round 9 of the 18 seam
  edges cleanly; the ones it rejected run into those trimmed flats. The peak (10.3 MPa at the finer 2.5 mm mesh that the fillet's small faces needed) is now at a
  trim corner right beside the fixed support, where a sharp corner meets a fully clamped face: a
  singularity, not a real stress. Away from it the forearm sits at the 3 MPa nominal. Rounding those trim
  corners properly needs the hub widened to the tube's 80 mm, which the J3 actuator's position doesn't allow
  as modelled.
- **The links are stiffness-limited, not strength-limited.** Every peak, real or singular, is more than
  25× below yield.

## Vibration (modal)

| Part | Support | First natural frequency | Hand check |
|---|---|---|---|
| Upper arm, link alone (rev 5, sharp seam) | Shoulder face fixed | 488 Hz | 499 Hz (cantilever tube, 2 % apart) |
| Upper arm, link alone (rev 10, filleted) | Shoulder face fixed | 530 Hz | 499 Hz (6 % apart: the fillets stiffen the root, which the formula ignores) |

This is the bare link. With the distal 13.6 kg lumped at the elbow and the stiffness from the static run
(3.6 N/µm), the link's own contribution is about 81 Hz. In a real arm the gearboxes are much softer than
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

**Revision 11:** nothing overlaps at rest or at the `flourish` pose (136 instance pairs). The fillets
added no new contacts. The only finding is a 0.06 mm³ contact between wrist 1 and J5, a seated pair,
which is numerical contact rather than interference.

## Collisions across the range of motion

| Study | What it checks | Revision 4 | Revision 5 | Revision 11 |
|---|---|---|---|---|
| `pick_and_place` animation check | 48 samples of the animation | clear (2 pairs overlapping at rest) | clear | clear |
| `pick_and_place_keys` | 12 key poses, near misses < 5 mm | 0 collisions | 0; closest 1–2 mm | 0; closest 0.5–2 mm (designed gaps) |
| `shoulder_elbow` | J2 × J3 grid, 20° steps over the limits | 35 of 204 collide | 0 of 132 | 0 of 132 |
| `arm_pitch` | J2, J3, J4 random, 150 poses (seed 1) | 32 % collide | 9.3 % (fingers into upper arm) | 0.7 %: 1 pose, J6 grazes the pedestal by 0.7 mm |

- **Elbow (J3) limit.** It was ±160°. Between +40° and +130° the wrist folded into the shoulder actuator
  and upper arm, up to 65 mm deep. The limit is now **−160° to +30°**, and the J2 × J3 grid is clear
  across its whole range.
- **Wrist pitch (J4) limit.** In revision 5, with J4 at about +90° to +130°, the gripper fingers reached
  back into the J3 actuator or the upper arm (up to 15.6 mm deep, 9.3 % of poses). A limit of +80°
  (revision 10) cut that to one pose in 150: J4 at +72° with the elbow near its +30° stop, still 5.7 mm into
  the upper arm. The limit is now **−180° to +60°**, and no pose in the sweep reaches back into the arm. The
  pick-and-place motion uses J4 from −45° to +55°, so it is unaffected.
- **What's left is the floor, not the arm.** The one colliding pose (J2 +91°, J3 +24°, J4 +53°) has the
  arm reaching forward and down past its own base, and the J6 actuator touches the pedestal's top edge by
  0.7 mm. That depends on the whole pose, not one joint, so it belongs in the controller's workspace
  limits (a keep-out box around the pedestal and the bench), as on any real arm.

## What these tests don't cover

- **Joint internals:** no gearbox, bearing, bolt or joint stiffness. The actuators are exterior shells.
- **Analysis types:** no fatigue, buckling, dynamic or impact loads, contact or plasticity. The loads
  are 1 g static; real accelerations add load roughly in proportion.
- **Not checked by simulation:** the cast base, the turret and the gripper. They are multi-body
  components, which STEVE's single-solid studies can't solve as modelled.
- **Not a certification.** These are idealised linear-elastic estimates.
