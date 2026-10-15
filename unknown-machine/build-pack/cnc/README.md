# CNC build pack: machined parts

Everything a job shop needs to quote and make the actuator's machined parts: one sheet per part (material,
finish, process and setups, stock, every critical feature with its tolerance and the reason, threads, inspection)
and a STEP file per part in [`step/`](step/).

- **Source:** STEVE design `02e31a10-ac9e-489a-8c91-1a4ce6a43b71` **revision 48** (mirrored in `../../source/`), with
  the linked parts carrier rev 8, carrier disk rev 5 and pedestal rev 8.
- **STEP files** are in the design frame (mm; motor axis +Z, output at +Z, pedestal toward −Y) and sit where the
  part goes in the assembly, except `planet.step` and `standoff.step`, which are at their own origin.
- **General notes for every drawing:** general tolerances ISO 2768-mK; edges ISO 13715 −0.3 (break 0.2–0.4 mm)
  unless a chamfer is shown; threads ISO metric coarse, 6H internal / 6g external, depths are full-thread depths;
  surface finish Ra 3.2 unless noted; remove all burrs, especially in bores and holes that carry cables or
  bearings. Fits are ISO 286.
- **The gears** (sun, planets, ring) go to a gear shop: the STEP teeth are a reference shape with the standard
  0.38 m root fillet; the gear data tables in their sheets are what to cut to. The CNC shop can supply the blanks.
- Quote quantities: 1 and 5 actuators.
- **Drawings:** one ISO first-angle PDF per made part in [`drawings/`](drawings/) (AM-01 to AM-15, revision A,
  ISO 2768-mK), dimensioned from the same STEP files; the STEP governs undimensioned geometry. Their source
  (Python, pythonocc + matplotlib, run with FreeCAD's bundled Python) is in [`drawings/source/`](drawings/source/):
  `/Applications/FreeCAD.app/Contents/Resources/bin/python drawings/source/build_all.py` rebuilds them all.

| Part | Drawing | Sheet | Qty | Material | Process | Setups (3-axis / turn-mill) | Finish |
|---|---|---|---|---|---|---|---|
| Motor housing | [AM-01-housing](drawings/AM-01-housing.pdf) | [housing.md](housing.md) | 1 | 6061-T6 | Turn-mill | 4 / 2 | Black anodise Type II, fits masked |
| Rear end bell | [AM-02-end_bell](drawings/AM-02-end_bell.pdf) | [end_bell.md](end_bell.md) | 1 | 6061-T6 | Turn, drill/tap | 3 / 2 | Black anodise Type II, fits masked |
| Encoder cap (fluted) | [AM-03-rear_cap](drawings/AM-03-rear_cap.pdf) | [rear_cap.md](rear_cap.md) | 1 | 6061-T6 | Turn-mill with C-axis (flutes) | 5 / 2 | Black anodise Type II |
| Front flange | [AM-04-front_flange](drawings/AM-04-front_flange.pdf) | [front_flange.md](front_flange.md) | 1 | 6061-T6 | Turn, drill | 3 / 2 | Black anodise Type II, fits masked |
| Pedestal | [AM-05-pedestal](drawings/AM-05-pedestal.pdf) | [pedestal.md](pedestal.md) | 1 | 6061-T6 | 3-axis mill (saddle by circular interpolation) | 5 / 3 on a 4th axis | Black anodise Type II, saddle chromate |
| Planet carrier, rear part | [AM-06-carrier](drawings/AM-06-carrier.pdf) | [carrier.md](carrier.md) | 1 | 303 stainless | Turn + 3-axis mill (posts from the front) | 3 | Passivate |
| Planet carrier, front disk + output hub | [AM-07-carrier_disk](drawings/AM-07-carrier_disk.pdf) | [carrier_disk.md](carrier_disk.md) | 1 | 303 stainless | Turn, drill/tap | 3 / 2 | Passivate |
| Output-bearing clamp ring (new) | [AM-08-bearing_clamp](drawings/AM-08-bearing_clamp.pdf) | [bearing_clamp.md](bearing_clamp.md) | 1 | 303 stainless | Turn | 2 | Passivate |
| Motor shaft (hollow) | [AM-09-motor_shaft](drawings/AM-09-motor_shaft.pdf) | [rotor.md](rotor.md) | 1 | 42CrMo4 +QT (4140 HT) | Turn, deep-drill both ends, mill flats, induction-harden, grind | 3 + grind | Black oxide, journals ground |
| Rotor hub sleeve | [AM-10-rotor_hub](drawings/AM-10-rotor_hub.pdf) | [rotor.md](rotor.md) | 1 | C45 | Turn | 2 | Black oxide, bond face masked |
| Encoder hub (new) | [AM-11-encoder_hub](drawings/AM-11-encoder_hub.pdf) | [encoder_hub.md](encoder_hub.md) | 1 | 303 stainless | Turn, drill/tap | 2–3 | Passivate |
| Readhead standoff (new) | [AM-12-standoff](drawings/AM-12-standoff.pdf) | [standoff.md](standoff.md) | 4 | 303 stainless | Swiss / bar lathe | 1–2 | Passivate |
| Sun gear m1 18 T | [AM-13-sun](drawings/AM-13-sun.pdf) | [sun.md](sun.md) | 1 | 18CrNiMo7-6 | Gear shop: turn blank, hob, carburise, grind, wire-EDM bore | — | Carburised 58–62 HRC, ground |
| Planet gear m1 27 T | [AM-14-planet](drawings/AM-14-planet.pdf) | [planet.md](planet.md) | 3 (+1) | 18CrNiMo7-6 | Gear shop: hob, carburise, grind teeth and bore | — | Carburised 58–62 HRC, ground |
| Ring gear m1 72 T internal | [AM-15-ring_gear](drawings/AM-15-ring_gear.pdf) | [ring_gear.md](ring_gear.md) | 1 | 34CrNiMo6 +QT | Gear shop: turn, shape (or wire-EDM) | — | QT 28–34 HRC, nitriding optional |

Bought parts (bearings, screws, dowels, retaining rings, encoder, motor) are in `../hardware/bom.csv`. Raw-stock
sizes and prices: `../hardware/stock.md`. Gear sourcing: `../hardware/gears.md`.

## Bearing fits at a glance

| Bearing | Housing (part) | Shaft (part) | Basis |
|---|---|---|---|
| IKO CRBH 3510 crossed roller, 35 × 60 × 10 | Ø60 H7 (housing), clamped by the clamp ring | Ø35 h5 (carrier sleeve), shoulder + DIN 471 35 | IKO recommended fits, rotating inner ring, normal load |
| 6001-2RS, 12 × 28 × 8 | Ø28 K7 (end bell, aluminium), DIN 472 28 | Ø12 k5 (shaft), 2 × DIN 471 12 | Stationary outer ring in light alloy: one step tighter |
| INA HK1210 drawn cup, 12 × 16 × 10 | Ø16 N6 (carrier, 303) | Ø12 h6 raceway on the shaft, ≥ 55 HRC | INA: N6 in steel housings, h6 raceway |
| INA HK0609 drawn cup, 6 × 10 × 9 (× 3) | Ø10 N6 (planet, ground after carburising) | 6 m6 hardened dowel pin as raceway | INA: N6; note the m6 pin on clearance |
| Stator (Kollmorgen KBM-17H01) | Ø85.100 +0.035/0 (housing), 6 adhesive grooves 0.2 deep | — | Kollmorgen mounting guide, bonded |
| Ring gear in the flange | Ø86 H7 (flange) | Ø86 s6 (ring) + Loctite 638 | 0.036–0.093 interference |

## What the DFM review changed (STEVE revision 36 → 48)

STEVE's `cnc` check (inspect_model, 1.5 mm tool radius, metal) was run on every made part. Its findings and the
changes are listed at the end of each sheet. In short:

- Inside corners: relief grooves (0.3 × 0.3, turned) at every bearing and stator shoulder; R1 post-root and R0.4
  shoulder fillets on the carrier; round-ended flutes on the cap; R4-ended cable slot on the pedestal; R1.5 where
  the cap's bosses meet its wall; ISO 53 root fillet (0.38 m) on all gear teeth.
- Edges: lead-in chamfers on every bearing seat, pilot and press fit; outside edges broken; tooth-tip chamfers.
- Holes: 118° drill points modelled; tap-drill and full-thread depths specified; the radial housing holes need a
  spot face on the curved surface.
- Features added because the design needed them to be built: adhesive grooves in the stator bore, a clamp ring
  for the crossed-roller bearing (it also centres the flange and ring gear), shoulder + retaining-ring groove for
  its inner ring, DIN 471 / 472 grooves for the 6001, a double-D drive for the sun (no room for a key), the HK1210
  seat corrected to Ø16, screws for the end bell and the rear cap, and the encoder (RLS AksIM-2) hub and standoffs.
- Left as is, with the reason in the sheet: the 15 × D shaft bore (drill from both ends), the pedestal's
  feather-edge where its screw holes exit the curved saddle, undercut faces the 3-axis check can't reach (they
  are lathe grooves), the gear teeth (gear shop), the rear-cap flutes (C-axis).

## Open questions for the designer (not machining issues)

- Thermal pad or paste in the saddle: the +0.00/+0.03 saddle bore leaves no room for the 0.23–0.25 mm pad in the
  BOM. Paste is assumed in the sheets.
- Planet pins (m6) as needle raceways take up part of the HK0609's clearance: check with INA or buy h6 pins.
- Shaft hardness at the HK1210 journal: 4140 gives about 55 HRC (reduced rating); 16MnCr5 carburised gives 58+.
- RLS readhead connector and its plug: not modelled; check the cap cavity and the cable exit against RLS's STEP.
