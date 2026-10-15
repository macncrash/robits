# Motor housing

STEP: [`step/housing.step`](step/housing.step) (assembled position, mm; motor axis +Z, output at +Z, pedestal at −Y).
Source: `source/components/housing.py`, STEVE design revision 48.

| | |
|---|---|
| Quantity | 1 per actuator |
| Material | 6061-T6 (T6511 extruded bar is fine), EN AW-6061 T6 |
| Stock | Ø5" (127 mm) round bar × 90 mm (one 12" bar also gives the front flange and the end bell; see `../hardware/stock.md`) |
| Finish | Black anodise, MIL-A-8625 Type II Class 2, 8–12 µm. **Mask** (chromate conversion, MIL-DTL-5541 Type II Class 3, instead): Ø85.10 stator bore and its grooves, Ø60 bearing seat and floor, Ø90 counterbore, Ø120 and Ø96 saddle diameters (thermal joint to the pedestal), all tapped holes (or chase them after anodising), dowel holes |
| Process | Turn-mill: op 10 rear (bore, grooves, ledge, fins, rear face), op 20 front (Ø120, Ø60 seat, Ø90 counterbore, front face), then the axial holes (live tooling, C-axis), radial holes from −Y (Y-axis or a 4th-axis/3+2 mill). 2 lathe setups + 2 milling setups on a 3-axis mill, or 2 setups on a turn-mill with main and sub spindle |
| General tolerance | ISO 2768-mK. Edges ISO 13715 −0.3 (break 0.2–0.4 × 45°) unless shown |

## Critical features

| Feature | Size and tolerance | Why |
|---|---|---|
| Stator bore (datum **A**), z −36..29 | **Ø85.100 +0.035/0**, cylindricity 0.02, Ra 1.6 | Kollmorgen KBM-17H01 stator OD 84.963: 0.07 mm radial slip fit for the bonded joint (Kollmorgen mounting guide, catalog pp. 90–95). Not polished: the bond needs Ra 1.6–3.2 |
| Adhesive grooves in the stator bore | 6 grooves, 5.0 wide, **0.20 ±0.05 deep** (Ø85.50 ±0.10), pitch 9, from z −26 to 24 | Kollmorgen asks for 0.13–0.26 mm grooves over at least half the bond length: 30 of 57.8 mm. Internal grooving tool from the rear |
| Depth-stop ledge Ø81, face at z 29 | Ø81.0 ±0.1; face perpendicular to A within 0.03 | Locates the stator axially, 2 mm off the bulkhead (Kollmorgen's minimum end-turn clearance). 0.3 × 0.3 relief in the corner so the stator banks square |
| Crossed-roller seat (CRBH 3510 outer ring), z 32.5..42.5 | **Ø60 H7 (+0.030/0)**, floor at 11.50 −0.02/0 below the front face; runout of Ø60 and of its floor to A ≤ 0.015; Ra 0.8 | IKO's recommended housing fit for CRBH with a rotating inner ring and normal load is H7 (check against the bearing actually bought). The coaxiality with A sets the motor air gap and the gear centre. 0.3 × 0.3 corner relief at the floor; 0.5 × 45° lead-in |
| Clamp-ring counterbore, front face | **Ø90 H7 (+0.035/0)**, 1.60 ±0.02 deep (floor 0.10 below the bearing's front face); coaxial with Ø60 within 0.015 | Holds the bearing clamp ring, which also centres the front flange and the ring gear. Turn in the same setup as Ø60 |
| Front face (flange seat), z 44 | Flatness 0.02; perpendicular to A within 0.02 | Flange and ring gear squareness to the output axis |
| Front section Ø120 and fin tips Ø96 (saddle diameters) | **Ø120 g6 (−0.012/−0.034)**, **Ø96 g6 (−0.012/−0.034)** | Sit in the pedestal saddle bored +0.00/+0.03: 0.012–0.064 mm diametral clearance, filled with thermal paste. (A 0.23–0.25 mm pad needs about 0.5 mm more clearance: decide pad or paste before machining the pedestal) |
| Rear spigot bore entry | 0.5 × 45° lead-in | End bell spigot and stator go in from the rear |
| 4 × M5 axial, PCD 100 at 45°/135°/225°/315° (flange screws) | **M5-6H, 15 full thread**, tap drill Ø4.2 × 18 (118° point). Position Ø0.2 to A | ISO 4762 M5 × 30 engages 14.5 mm (2.9 d) |
| 4 × M5 radial from −Y at x ±16, z 28 and 37 (pedestal screws) | **M5-6H, 12 full thread** measured from the curved surface (y −57.8); drill Ø4.2 to y −43.5 (+ point). Position Ø0.2 | M5 × 20 from below engages about 11 mm. **The drill enters a surface inclined at 15.5°: spot it with a Ø5 flat end mill first** |
| 2 × Ø4 radial from −Y on the centre line, z 22 and 40 (dowels) | **Ø4 H7 (+0.012/0)**, 6 min deep (drilled 8 + point). Position ±0.01 to each other and to A, measured with the pedestal's dowel holes | ISO 8734 / DIN 6325 4 m6 dowels, pressed in the pedestal, slip fit here so the housing lifts off |
| 4 × M4 in the rear face, PCD 92 at 45°/135°/225°/315° (end-bell screws) | **M4-6H, 9 full thread**, tap drill Ø3.3 × 10.5 (+ point). Position Ø0.2 to A | ISO 4762 M4 × 16 engages 8.5 mm (2.1 d) |

## Inspection

- CMM: Ø85.10 bore (several heights), Ø60 seat, Ø90 counterbore, runouts to A, front-face flatness, hole positions.
- Groove depth: a groove gauge or a profile replica on one groove.
- Thread GO/NO-GO gauges after anodising (or after chasing).
- Test the dowels in the pedestal: the housing must drop into the saddle and lift off without force.

## DFM review (STEVE `cnc` check, revision 36 → 48)

| Finding | Change |
|---|---|
| No adhesive grooves in the stator bore (README asks for them) | Added 6 × 5 × 0.2 grooves |
| Sharp corners at the bearing floor and the stator ledge | 0.3 × 0.3 relief grooves (turned) |
| No lead-in or edge breaks | 0.5 × 45° on the bore entry, the bearing seat and the outside corners; ISO 13715 note for the rest |
| Holes 4.3 × D deep, flat-bottomed in the model | Kept the depth (thread needs it); 118° drill points modelled |
| Flange (and ring gear) only located by screws in clearance holes (±0.25 mm) | Ø90 counterbore and a clamp ring centre them on the bearing axis |
| Crossed-roller outer ring had no axial retention | Seat moved 1.5 mm deeper; the clamp ring under the flange holds it |
| End bell had no fasteners | 4 × M4 tapped in the rear face |
