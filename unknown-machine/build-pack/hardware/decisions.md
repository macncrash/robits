# Decisions the design was missing: servo drive and motor encoder

Researched on 2026-10-14. Nothing was ordered and no vendor was contacted. Where a fact could not be seen on a
source page, it is marked **not verified**.

## 1. Servo drive: Kollmorgen AKD-P00306-NBAN-0000 (or the current NCAN/NDAN equivalent)

### Choice

**AKD-P00306-N?AN-0000.** Reading the code: P = Position Indexer, 003 = 3 A rms, 06 = 120/240 Vac 1~/3~,
N? = no option card (the hardware generation is NA, NB, NC or ND), AN = analog connectivity, 0000 = standard.

- Several resellers list **AKD-P00306-NBAN-0000**, and Wake Industrial lists **AKD-P00306-NCAN-0000**.
- A search snippet said Radwell marks NBAN as discontinued, replaced by **AKD-P00306-NDAN-0000**. This is
  **not verified** (Radwell blocked the page). Ask the distributor which generation is current.
- Don't order the B (Base) version. The 2022 installation manual's type key gives B as "SynqNet only".
  The P version has the analog input, the encoder emulation and the full I/O.
- AKD-M is EtherCAT only and doesn't fit.

Source: *AKD Installation Manual*, Kollmorgen 903-200003-00, edition AG (May 2022), §6.3 type key p. 33.
Official URL: https://www.kollmorgen.com/sites/default/files/public_downloads/903-200003-00%20AKD_Installation_en%20Rev%20AG.pdf
(the Kollmorgen site blocks scripts, so a verbatim mirror was read:
https://www.kml-technology.com/wp-content/uploads/2024/05/Kollmorgen_AKD_Installation_EN.pdf).

### How it meets the requirements

| Requirement | AKD-x00306 (manual §7.6 p. 39 unless noted) | OK? |
|---|---|---|
| 240 Vac single-phase input | 1 × 100–240 V ±10 %, 50–400 Hz. Single-phase is allowed for x00306–x01206: wire L1/N and leave L3 open (§9.8.4.2 p. 111). Input current 5.0 A at 1 × 240 V | yes |
| Continuous 3.11 A rms | Rated **3 A rms** continuous at 40 °C (derates 4 %/K above 40 °C) | **3 % short.** The motor's continuous rating is 3.11 A, but the housing limits continuous current anyway: about 1.3–2 N·m, 2–3 A (analysis/README.md). Set the continuous limit to 3.0 A |
| 5.9 A peak limit | 9 A rms peak for 5 s. Set the drive's peak current (IL.LIMITP) to 5.9 A | yes |
| PTC thermistor | MOTOR.RTYPE 0 = PTC, MOTOR.TEMPFAULT sets the trip resistance. PTC goes to X10 pins 8/9 **for incremental, EnDat, Hiperface and BiSS-B feedback** | **open question with BiSS-C, see below** |
| ±10 V analog speed command | X8/10 (+) and X8/9 (−), differential ±12.5 V, 16 bit, > 13 kΩ. DRV.OPMODE 1 (velocity), DRV.CMDSOURCE 3 (analog), AIN.VSCALE in rpm/V | yes |
| 24 V enable input | X8/4 = DIGITAL-IN 8 = ENABLE, fixed function, active high, 3.5–30 V on | yes |
| Fault output | Fault relay X8/1–X8/2, closed when there is no fault (DOUT.RELAYMODE 0), 30 Vdc / 1 A | yes |
| STO | X1/3, 24 V, 45 mA, SIL 2 / PL d single channel | yes |
| Encoder emulation, A/B RS-422 | X9 (D-sub 9 male), A/B/Z RS-485 line drivers, up to 3 MHz. DRV.EMUEMODE 1, DRV.EMUERES in lines/rev | yes |
| Feedback | X10 (D-sub 15 HD female). FB1.SELECT 34 = BiSS-C (digital), 10 = incremental + Halls, plus EnDat 2.2, Hiperface (DSL), SFD, resolver and sine/cosine | yes |
| Motor inductance | Minimum **2.5 mH** at 240 V (1.3 mH at 120 V), maximum 250 mH | **not verified**: take the KBM-17H01-B00 line-line inductance from the KBM catalogue or its data sheet |

Size: 54 × 200 × 185 mm (W × H × D with connectors), 1.1 kg, no fan. It needs a separate 24 V ±10 % supply
at 0.5 A (no brake). There is no internal regen resistor. An external one (33 Ω, AKD-x00306) is needed only
if the arm brakes hard: the 5:1 stage and a small arm make a light load, so try without one and watch the
bus over-voltage fault.

### Open question: motor PTC with BiSS-C feedback

The X10 pin table in the 2022 manual (p. 122) lists Th+/Th− on pins 8/9 for incremental, BiSS-B, EnDat 2.1 and
Hiperface, but shows "–" for **BiSS-C**. So the AKD may not read the motor PTC when BiSS-C is selected.
Two ways forward:

1. **Ask Kollmorgen** whether MOTOR.TEMPFAULT works on X10/8–9 with FB1.SELECT 34. The AksIM-2 cable carries
   two spare isolated wires for exactly this (readhead pins 3/4). The PTC can then run in the encoder cable
   to X10/8–9 at no extra cost if the answer is yes.
2. **Fallback that doesn't depend on that answer:** fit a PTC thermistor relay (DIN-rail, for a standard
   PTC chain) in the cabinet. Its output contact goes into a programmable digital input (e.g. X7/4 =
   DIN3, DIN3.MODE = controlled stop, or fault) or opens the ENABLE line. The part number is not chosen yet
   (to-confirm in `bom.csv`). Check that the relay's trip resistance matches the KBM PTC (Kollmorgen
   publishes the PTC's resistance–temperature curve with the KBM catalogue).

### Price seen

No authorised-distributor price was visible. These reseller prices were seen for AKD-P00306-NBAN-0000 on
2026-10-14:

| Seller | Price (USD) | Condition | Status |
|---|---|---|---|
| servosupplier.com/products/akd-p00306-nban-0000 | 2,473.00 | unused surplus | seen on the page |
| ServoSupplier | 744.84 | refurbished | seen on the page |
| surplusselect.com | 309.99 | used | seen on the page |
| Radwell | about 4,024 new | | search snippet only, not verified |
| iAutomation | 1,150 | backordered | search snippet only, not verified |

Use a new or unused drive from an authorised Kollmorgen distributor for a product build pack, and get a
quote. The BOM carries 2,473 USD (the unused unit seen) as the price, status to-confirm.

### Cheaper alternative: Servotronix CDHD2-0032AAP1

Reading the code: 003 = 3 A rms continuous / 9 A peak (2 s), 2A = 1-phase or 3-phase 120/240 V, AP1 =
analog, pulse and RS-232 command. On paper it meets everything, and unlike the AKD it reads **PTC or NTC
together with BiSS-C** (up to 26 bit), on C4 pins 12/25.

- ±10 V analog in: C2/8 (+), C2/26 (−).
- A/B/Z RS-422 encoder output: C2/22, 4, 23, 5, 24, 6, up to 5 MHz.
- Fault relay: C3/10, C3/20.
- STO: P1.
- 24 V inputs.

Its drawbacks:

- Servotronix calls it a **legacy product**.
- The user manual says **STO certification is pending** for all CDHD2 models.
- It needs a separate AC logic supply on L1C/L2C.
- The only price seen was a search-result eBay listing of about 1,000 USD, which is not verified.

Use it only if the AKD's PTC/BiSS-C answer is no and the PTC relay workaround isn't wanted. Sources: CDHD2
Quick Start Guide rev 1.4 and User Manual fw 2.38.x
(https://www.stxim.com/wp-content/uploads/2024/01/CDHD2_QSG_fw_2.15.x_Rev_1.4.pdf,
https://www.stxim.com/wp-content/uploads/2024/01/CDHD2_User_Manual_fw2.38.x_Rev_2.6-i.pdf).

Not researched: Copley Xenus Plus, Elmo and Ingenia drives.

## 2. Motor feedback encoder: RLS AksIM-2 size 039, BiSS-C

### Choice

- **Readhead MB039DCC18BENT00**
- **Ring MRA039BC020DSE00**
- Cable: **ACC049** (1 m, flying leads) or **ACC070** (3 m, flying leads)

RLS d.o.o. (Slovenia, a Renishaw associate company). Datasheet: *AksIM-2 off-axis rotary absolute encoder*,
MBD01_15, 13 May 2026, https://cdn.rls.si/documents/datasheets/MBD01.pdf (ordering codes pp. 47–50).
Ring installation guide: https://cdn.rls.si/documents/datasheets/MRAD01.pdf. 3D models:
https://cdn.rls.si/documents/cad-models/MB039_MRA039_3D_files.zip.

It replaces the placeholder code disk (`encoder_disk`) and read head (`read_head`). Both of those are deleted
from the build.

Why this one:

- It is absolute single-turn, so it gives commutation and position from one cable and needs no Halls.
- It reads off-axis through a ring, so the Ø8 cable bore stays open.
- Size 039 is the only AksIM-2 size whose ring screws to a small hub and whose readhead still clears a Ø12
  shaft.
- It fits the Ø78 × 14 rear-cap cavity with about 2 mm axial and 12 mm radial margin.
- RLS sells it from an online shop with visible prices.

Sizes rejected:

- MB029: its rings have a Ø10 bore, or a Ø12.7 p7 press fit, so a Ø12 shaft can't carry them. A sleeve from
  12 to 12.7 would be 0.35 mm thick.
- RLS Orbis: on-axis, with the magnet on the shaft end, so it can't work with a through-bore shaft.
- Same Sky AMT31: bores of 2–8 mm only.
- Netzer DS-25: Ø6 bore.

### Ordering codes

| Readhead `MB039DCC18BENT00` | Meaning |
|---|---|
| MB | AksIM-2 board readhead |
| 039 | for the MRA039 ring |
| DC | BiSS-C, RS-422 |
| C | bidirectional, register access |
| 18B | 18 bit single-turn. 17B, 18B and 19B are offered for size 039; the datasheet says only 17 bit is noise-free on MRA039. **17B (MB039DCC17BENT00) is the conservative choice**; 18B gives 262,144 counts/rev |
| E | partial-arc shape, tangential connector exit (the only shape for 039) |
| N | FCI/AMP 10114830-11108LF 8-pin horizontal connector |
| T | −40 to +105 °C |
| 00 | no special |

| Ring `MRA039BC020DSE00` | Meaning |
|---|---|
| MRA | AksIM magnetic ring |
| 039 | Ø39 OD |
| B | 2.0 mm thick |
| C | countersunk screw holes |
| 020 | Ø20 bore |
| D | standard accuracy, stamped |
| S | stamped AISI 430 plate with CPE (rubber magnet) layer |
| E | engraved zero mark |
| 00 | no special |

### Dimensions for the CAD (mm)

**Ring MRA039BC020DSE00**

- OD Ø39 ±0.1, bore Ø20 H7 (+0.021/0), thickness 2.0 ±0.05.
- It is made of a steel plate and a rubber magnet layer. The drawing shows a 1.2 mm step between the two;
  take the layer split from the STEP model.
- The magnetic face is the rubber face. It must be parallel to the mounting face within 0.05.
- 8 × countersunk holes for **M2 ISO 7046** flat-head screws on a **Ø25 PCD**, every 45°.
- RLS recommends a **g6 pilot**, so make the hub pilot Ø20 g6. Adhesive is optional.
- Which face carries the countersinks: **not verified**. Read it from the RLS STEP model.
- Maximum speed 10,000 rpm; the motor runs at 3,000–5,300 rpm.

**Readhead MB039DCC18BENT00**

- A partial-arc PCB: 196° ±0.2° of an annulus, outer radius **R27 ±0.1 (Ø54)**, inner radius **R10.6 ±0.1
  (Ø21.2)**. The selection table says the readhead ID is 23. Model R10.6 and check it against the STEP model.
- Across the arc chord it measures about 54 wide × 31 deep (estimate).
- PCB 1.6 ±0.2 thick. The height from the mounting surface to the top of the components is **5.2 ±0.3**.
- **Mounting:** 4 × Ø2.2 through holes for **M2** screws, with Ø4.2 plated pads, on **R24.5 (Ø49 PCD)**, at 0°,
  60°, 120° and 180°. The 0° and 180° holes lie on the arc's straight-edge centreline.
- **Mounting surface:** the gold-plated annulus R20–R27 on the sensor side. Keep standoffs and pads outside R20.
- **Sensor:** about 15 mm wide, centred in the arc.

**Installation tolerances (datasheet)**

| Item | Value |
|---|---|
| Ring mounting face to readhead mounting surface (axial) | **2.88 ±0.13** |
| Ride height, rubber face to sensor | **0.23 ±0.18** (general range 0.05–0.35) |
| Radial offset | ±0.4 |
| Tangential offset | ±0.3 |
| Tilt | < 0.2° |
| Shims | RLS MB-ACC shims for size 039 |

The readhead has a status LED (green when the ride height is right). The ride height can also be read over
BiSS, registers 0x4E–0x4F.

**External magnetic field.** No more than 20 mT at the ring; 50 mT damages it. The rotor magnets end at
z −15 and the ring sits at about z −44 to −46, so about 30 mm separates them. The stator end turns are
closer. Check the field with a gaussmeter at first assembly. If it reads high, put a thin steel shield
disk (for example 0.5 mm, 1008 or 430) between the end bell and the ring.

**Proposed stack.** Here z is measured from the end bell's rear face (design z −48), positive rearward, into
the cap.

| Item | z (from the end bell rear face) | Design z |
|---|---|---|
| New **encoder hub** on the shaft: Ø12 H7 bore, set screw or clamp plus Loctite 641 if wanted; flange Ø30 × 3 with M2 tapped holes on PCD 25; Ø20 g6 pilot about 1.8 long. Anything behind the ring must stay under Ø21.2 to clear the readhead | 0.5 – 3.5 (flange) | −48.5 to −51.5 |
| Ring mounting face / ring magnetic face | 3.5 / 5.5 | −51.5 / −53.5 |
| Readhead mounting (gold) surface, sensor side facing forward toward the ring: ring mounting face + **2.88 ±0.13** (RLS figure, which includes the ring thickness, the sensor package height and the 0.23 ride height). Mounted on 4 standoff posts about Ø4 × 6.4 tall, screwed to the end bell's rear face at R24.5, with M2 screws. That leaves about 3 mm radial clearance to the Ø39 ring. Shim until the LED is green | 6.38 | −54.38 |
| Top of the readhead components | about 11.6 (11.9 at worst tolerance) | about −59.6 |
| Shaft end | 12 | −60 |
| Cap inner floor | 14 | −62 |

The PCB's sensor side faces the ring, so its components sit between the PCB and the ring. Check
in the RLS STEP model which way the 5.2 mm component height stacks. If the components are on the far side
of the PCB, the top of the readhead is at about z 11.6 as shown. If they are on the ring side, the readhead
ends near z 8 and the margin grows.

Margins: about 2.1 mm axially to the cap floor, and Ø54 inside Ø78 radially. That leaves 12 mm for the
connector, whose cable leaves tangentially. The mating plug height on the horizontal connector is **not
verified**; take it from the STEP model.

### Electrical

- **Supply:** 4.5–5.5 V, 130 mA typical, 150 mA maximum. The AKD X10 supplies +5 V (BiSS-C mode: 5.1 V ±5 %,
  up to 350 mA).
- **Readhead connector:** FCI/AMP **10114830-11108LF** (8 pin). Mating housing **10114826-00008LF** and
  contacts **10114827-002LF**. The RLS cable comes with it fitted.
- **BiSS-C:** clock up to 5 MHz (the AKD runs it at 1 MHz), point to point. The frame is position, then
  nError and nWarning (active low), then CRC-6 (polynomial 0x43), the same layout as Renishaw RESOLUTE.

| AksIM-2 pin | Signal | RLS cable wire | AKD X10 pin (D-sub 15 HD) |
|---|---|---|---|
| 1 | +5 V | brown | 10 (+5 V) |
| 2 | 0 V | white | 11 (0 V) |
| 3 | Temperature sensor 1 (isolated pass-through) | pink | 8 (Th+): only if Kollmorgen confirms PTC with BiSS-C; otherwise wire to the PTC relay |
| 4 | Temperature sensor 2 | grey | 9 (Th−): same |
| 5 | MA+ (clock) | red | 2 (CLK+) |
| 6 | MA− | blue | 3 (CLK−) |
| 7 | SLO+ (data) | green | 6 (DAT+) |
| 8 | SLO− | yellow | 7 (DAT−) |
| — | shield | shield | connector shell |

Also wire **SEN+ / SEN− (X10 pins 4 / 5)** to +5 V / 0 V at the encoder end so the drive senses the supply
there. This follows the AKD's BiSS-C wiring diagram (§9.12.8.2); check it against the manual at build time.

- **Cable:** RLS cable, 4 × 2 × 0.14 mm² twisted pairs, LiYCY, shielded, Ø6.2. The 1 m ACC049 reaches the
  pedestal port. A 3 m ACC070 or a separate extension cable runs to the drive.

### AKD settings and compatibility

- **FB1.SELECT = 34** (BiSS-C, digital). FB1.BISSBITS = the position bit count: 18 for the 18B readhead, 17 for
  17B. That value is inferred from the parameter definition and is **not verified**. Then disable the
  drive, clear faults and save.
- **Commutation alignment:** use the AKD's motor-phase finding (wake and shake, or the commutation alignment
  procedure in the user guide).
- **Compatibility risk:** AksIM-2 is not on Kollmorgen's "documented BiSS-C encoders" list. That list names
  RLS LMA10, Renishaw RESOLUTE and Hengstler. Kollmorgen warns that encoders with active-high error bits
  fail; AksIM-2's error bits are active low, like RESOLUTE's.
  - Expected to work, but bench-test it before building the pack around it, using RLS's E201-9B USB BiSS
    interface (€220) for zeroing and self-calibration.
  - Sources: https://webhelp.kollmorgen.com/AKD/English/Content/CommandParamRefGuide/FB1/FB1.SELECT.htm and
    https://www.kollmorgen.com/en-us/developer-network/what-types-biss-c-encoders-are-supported-akd-0. Both
    were read from search-indexed text because the site blocks scripts.

### Price seen (RLS online configurator, https://www.rls.si/eng/aksim-2-off-axis-rotary-absolute-encoder, 2026-10-14, EUR, VAT status not verified)

| Item | Price (EUR) |
|---|---|
| MB039 DC-C 18B readhead (17B: €141.70) | 152.60 |
| MRA039BC020DSE00 ring | 76.30 |
| ACC049 cable 1 m, flying leads (ACC070 3 m: €30) | 10.00 |
| MB-ACC shims for size 039, about €3.70 each, in multiples of 5 | about 18.50 |
| E201-9B USB BiSS interface (one per workshop, not per unit) | 220.00 |

### Cheaper fallback (not recommended): Same Sky (formerly CUI) AMT33 kit

- Part: **AMT332D-V**. The kit includes a 12 mm sleeve.
- Output: incremental A/B/Z plus U/V/W Halls as differential line drivers, read by the AKD with
  FB1.SELECT 10. In that mode the AKD reads the PTC on X10/8–9, so no PTC relay is needed.
- Problems:
  - It is 13.5 mm tall in a 14 mm cavity.
  - It needs at least 13.5 mm of shaft stub, and the shaft has 12 mm.
  - Accuracy is 0.2°.
- Price not verified.
- It would need a 1.5 mm longer shaft and a deeper cap.

## Changes these decisions force on the CAD

1. Delete `encoder_disk` and `read_head`.
2. Add the encoder hub, the MRA039 ring and the MB039 readhead (from the RLS STEP), 4 standoffs and
   M2 screws as above.
3. Add an exit for the encoder cable: from the cap cavity, through the end bell and the housing, to the
   pedestal side port. Or, since the Ø8 shaft bore is the cable path for the arm, add a separate cable
   slot in the end bell spigot.
4. The sun bore changes to a double-D (see `gears.md`).
5. Add fasteners that hold the end bell to the housing, and the rear cap to the end bell. Neither has
   fasteners in revision 36. See `bom.csv` lines 34–35. Also see line 39: nothing holds the crossed-roller bearing axially.
