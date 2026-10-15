# Machine control pendant (PCB + printed enclosure)

The operator's hand control for every machine driven by the [planetary joint actuator](../../README.md): the
manual lathe, the milling attachment, the bench grinder, the disc sander, the cold saw and the band saw in
[`lathe-kit/`](../../../lathe-kit/). Their READMEs say "the drive, the stop switch and the wiring aren't
modelled"; this pendant is the stop switch and the operator side of that wiring. One pendant serves any of the
machines: the machine is chosen in a setup menu, which sets the rpm scaling.

> **The pendant is not a safety device.** Its E-stop's first contact is wired straight through the board to the
> drive's **STO** input (Safe Torque Off) with no electronics in its path; the safety function is the drive's
> STO (on the AKD: SIL 2 / PL d, single channel). Everything else on the board (STOP, enable, the ramp to 0 V,
> the E-stop monitor) is functional control, built to fail towards "stopped", but it is not safety-rated.
> A risk assessment of each machine decides whether single-channel STO is enough.

STEVE documents (folder *Unknown machine / Build pack*):

| What | Document | Revision |
|---|---|---|
| Circuit (tscircuit) | [Machine control pendant PCB](https://stevecad.studio/?document=94f4bee3-1629-4a47-808e-e7974db7754d) | 32 — **Ready to order** (build 42dbef24) |
| Enclosure (CadQuery design, links the circuit) | [Machine control pendant enclosure](https://stevecad.studio/?document=4032528e-7594-4bb4-b2b7-6de9d52228b1) | 11 — fit check clear, links the circuit at revision 32 |

**Status (2026-10-15):** STEVE's readiness verdict for the circuit is **Ready to order** (0 blocking issues, 0
DRC errors, 84/84 connections routed, every trace at least 0.3 mm). Board: **80 × 110 mm, 4 layers, 1.6 mm, 116 placed
parts**. Nothing has been ordered. The enclosure's fit check is clear and its two printed parts are in
[`../print/pendant/`](../print/pendant/).

## What the board does

- Takes **24 V DC** from the drive's 24 V logic supply (or a DIN-rail supply) through the pendant cable.
- Outputs a **±10 V speed command** to the drive's analog input, ramped up and down by the firmware. It is held
  at **0 V by hardware** whenever the processor is not actively running the machine (reset, brown-out, crash,
  watchdog).
- Drives the drive's **ENABLE** input with a short-circuit-protected 24 V high-side switch. **STOP** and an
  opened **E-stop** pull the enable driver off in hardware, independent of the firmware.
- Reads the drive's **fault relay** ("drive OK") through an optocoupler.
- Passes **E-stop contact 1** straight through to the drive's STO and reads **E-stop contact 2**.
- Reads the drive's **encoder emulation** (A/B, RS-422) and shows **spindle rpm** on a 4-digit 14 mm LED display.
- Has a **speed knob**, a **FWD / OFF / REV** toggle, **RUN**, **STOP** and **JOG** buttons, and RUN / FAULT /
  power LEDs.
- **USB-C** for firmware and setup, and an SWD header footprint.

## Requirements (confirmed)

| # | Requirement | How it is met / how it is tested |
|---|---|---|
| R1 | Drives any servo drive with a ±10 V analog speed input and 24 V digital I/O; primary target Kollmorgen AKD (240 Vac) | Generic interface: differential-capable ±10 V output (CMD + AGND), sourcing 24 V enable, dry-contact or 24 V sourcing fault input, STO pass-through, A/B RS-422 input. `drive-interface.md` did not exist when the schematic was drawn, so the generic interface is used and the AKD pins below come from [`../hardware/decisions.md`](../hardware/decisions.md) (AKD installation manual 903-200003-00 rev AG). **Test:** AKD runs a motor from the pendant |
| R2 | 24 V DC, reverse-polarity and transient protected; on-board rails | 200 mA / 48 V PTC, SMBJ28A TVS (600 W), SS210 series Schottky; LMR16006X buck (60 V) to 5.15 V, AP2112K to 3.3 V, 78L15 to +15 V, NE555 charge pump to about −12.5 V. **Test:** reverse 24 V for 10 s, nothing hot, then normal start |
| R3 | Speed knob, FWD/OFF/REV, RUN, STOP, JOG; RUN latches enable through the MCU only with no fault and a healthy E-stop monitor; STOP always drops it | Knob on ADC_IN2; buttons and selector on GPIO with 10 k pull-ups. STOP also clamps the enable transistor's base through a BAT54 (hardware). **Test:** hold RUN with the MCU halted by SWD: no enable; press STOP while running: enable drops even with the firmware frozen |
| R4 | ±10 V bipolar, monotonic, few-mV resolution, ramped, 0 V when not running; 0 V and enable off on MCU reset / brown-out | MCP4822 (2 × 12 bit, internal 2.048 V reference) into an OPA2171 difference amplifier: CMD = 5.1 × (A − B), about 2.5 mV per step, ±10.4 V full scale; each direction is one DAC channel, so the output is monotonic through zero. A DG419 analog switch connects the terminal to the amplifier only while CMD_EN is driven high; its pull-down makes reset = terminal on 0 V. EN_REQ has a pull-down too. **Test:** hold RUN (MCU in reset): CMD terminal reads 0 V ± 5 mV and J1.3 reads 0 V |
| R5 | Enable output to a 24 V digital input (sourcing, short-circuit tolerant); fault input from the drive (24 V, opto-isolated or clamped) | BTS4140N smart high-side switch (current limit and thermal shutdown, 60 V), SMBJ28A at the terminal. Fault/drive-OK input through 10 k into a PC817, reverse-protected by a 1N4148W. **Test:** short J1.3 to 0 V while enabled: no damage, recovers |
| R6 | 22 mm mushroom E-stop, two NC contacts: #1 straight to STO with no logic, #2 read by the MCU | Contact 1 on J3.1–2, copper only (0.5 mm traces) to J1.6–7. Contact 2 on J3.3–4 to PB13 (low = healthy) and to Q3, which also holds the enable driver off. **Test:** E-stop pressed: drive shows STO active and the display shows `E-St` |
| R7 | RPM readout of the drive's encoder emulation (A/B RS-422, 5 V), shown on a display readable at 1 m; per-machine scaling in a menu stored in flash | Two SP3485 receivers with 120 Ω terminations into the MCU's TIM2 in encoder mode; TM1637 driving a 0.56 in (14.2 mm digit) common-anode display; lines/rev and ratio stored in the last flash pages. **Test:** set the drive's emulation to 1024 lines, compare with a tachometer |
| R8 | RP2040 or similar common part, SWD and USB-C | STM32F072C8T6 ("similar": a common JLCPCB part with internal flash and crystal-less USB; the RP2040 was drawn first, but its 0.4 mm QFN plus external flash and crystal would not autoroute cleanly on this board). USB-C with ESD array and the ROM DFU bootloader; SWD 5-pin footprint |
| R9 | Pluggable screw terminals or one locking connector for the pendant cable, on one edge | Two 8-way 3.81 mm pluggable terminal headers (J1, J2) plus USB-C, all on the bottom edge |
| R10 | About 90 × 150 mm hand-held; panel parts on top; E-stop on the top end | Board 80 × 110 mm. Enclosure **92 × 165 × 38.5 mm** — 15 mm longer than asked: the E-stop and its contact blocks sit above the board's top edge and the cable plugs need room at the bottom (see Open issues) |
| R11 | 5 prototypes, JLCPCB PCB + assembly, basic parts preferred | All parts pinned to JLCPCB numbers; see Parts and cost |

Assumptions (stated, not asked): the pendant cable is a 14-core screened cable (e.g. LiYCY 14 × 0.25 mm², about
8 mm) up to 5 m long; the encoder emulation runs at ≤ 1 MHz edge rate; the drive's analog input is differential
(as on the AKD); the shop is indoors, 5–40 °C, dry.

## Block diagram (in words)

```
24 V in (J1.1/2) -> PTC 200 mA -> TVS SMBJ28A -> SS210 ----> V24
   V24 -> LMR16006X buck -> 5.15 V -+-> B5819W -> V5 <- B5819W <- USB VBUS (J5)
                                     V5 -> AP2112K -> 3.3 V (STM32F072, DAC, RS-422 rx, inputs)
                                     V5 -> TM1637 display driver, DG419 logic supply
   V24 -> 78L15 -> +15 V -> NE555 ~70 kHz -> diode charge pump -> about -12.5 V
          (+15 / -12.5 V feed only the OPA2171 output amplifier and the DG419 switch)
   V24 -> BTS4140N high-side switch -> J1.3 ENABLE (24 V)     [Q2 driver; STOP (D9) and E-stop (Q3) hold it off]
   V24 -> J1.4 -> drive fault relay -> J1.5 -> 10 k -> PC817 -> PB12 (DRV_OK_N)

STM32F072 -SPI1-> MCP4822 (A = forward, B = reverse) -> OPA2171 difference amp ×5.1 -> 22 Ω -> DG419 S2
                                                       DG419 S1 = 0 V; D -> J2.1 CMD (+ SMAJ15CA)
       PB0 CMD_EN -> DG419 IN (100 k pull-down: reset = 0 V at the terminal)
J2.3..6 encoder A±, B± -> 120 Ω -> SP3485 ×2 -> PA0/PA1 (TIM2 encoder mode)
Knob -> PA2 (ADC); 24 V monitor -> PA3 (ADC); buttons, toggle (J4), E-stop contact 2 (J3) -> GPIO
TM1637 -> FJ5461BH 4-digit LED; LEDs: power (green), RUN (green), FAULT (red)
E-stop contact 1: J3.1/J3.2 <== copper only ==> J1.6/J1.7 -> drive STO loop
```

## Connectors and wiring to the drive

Board connectors (both pluggable terminal blocks are 3.81 mm pitch, WJ15EDGRC-3.81-8P headers; the mating
plugs are 15EDGK-3.81-08P or equivalent, 8-way, and are not assembled by JLCPCB: order them separately).

**J1 — power, enable, fault, STO** (pin 1 on the left, seen from the cable side)

| J1 pin | Signal | Cable | Kollmorgen AKD-P00306 | Generic drive |
|---|---|---|---|---|
| 1 | +24 V in | red | 24 V logic supply + (X1.1 on the AKD's 24 V connector, or the DIN-rail supply +) | 24 V supply + |
| 2 | 0 V | black | 24 V supply 0 V (X1.2) | 0 V |
| 3 | ENABLE out (24 V sourcing) | white | **X8.4** DIGITAL-IN 8 = ENABLE (active high, 3.5–30 V); its common **X8.3** (DCOM8) to 0 V | enable input + (its common to 0 V) |
| 4 | Fault-relay supply (+24 V out) | grey | **X8.1** fault relay contact | drive OK / fault output common |
| 5 | Drive OK in | grey/pink | **X8.2** fault relay contact (closed = no fault, DOUT.RELAYMODE 0) | drive OK output (24 V = OK) |
| 6 | STO loop A (E-stop contact 1) | yellow | 24 V supply + (feeds the STO through the E-stop) | STO supply / safety relay channel |
| 7 | STO loop B (E-stop contact 1) | yellow/green | **X1.3** STO input (24 V, 45 mA) | STO input |
| 8 | 0 V | brown | (spare 0 V, or the STO return where a drive needs one) | 0 V |

**J2 — analog command and encoder emulation**

| J2 pin | Signal | Cable | Kollmorgen AKD-P00306 | Generic drive |
|---|---|---|---|---|
| 1 | CMD (±10 V) | twisted pair 1 | **X8.10** Analog-In + | analog in + |
| 2 | AGND (0 V reference) | twisted pair 1 | **X8.9** Analog-In − | analog in − / AGND |
| 3 | Encoder A+ | twisted pair 2 | **X9/1** A+ | A+ |
| 4 | Encoder A− | twisted pair 2 | **X9/2** A− | A− |
| 5 | Encoder B+ | twisted pair 3 | **X9/4** B+ | B+ |
| 6 | Encoder B− | twisted pair 3 | **X9/5** B− | B− |
| 7 | Encoder 0 V | | **X9/3** GND | encoder 0 V |
| 8 | Screen | screen | drive's screen clamp; the pendant end is on 0 V | |

X9 pins are from `../hardware/drive-interface.md` (AKD Installation Manual §9.13.5.1): A+ 1, A− 2, GND 3, B+ 4, B− 5
(Z+ 7 / Z− 8 unused). Tie X8/7 (AGND) to X8/9 at the drive. AKD settings: `DRV.OPMODE 1`, `DRV.CMDSOURCE 3` (analog), `AIN.VSCALE` in
rpm/V (motor rpm at 10 V divided by 10), `DRV.EMUEMODE 1`, `DRV.EMUERES 1024` (or what the menu is set to), fault
relay `DOUT.RELAYMODE 0`.

**J3 — E-stop (JST XH 4-way, B4B-XH-A):** 1 = contact 1 in (STO loop A), 2 = contact 1 out (STO loop B),
3 = contact 2 (monitor), 4 = contact 2 return (0 V). Both contacts are NC. Wire with 0.25–0.5 mm² wire.

**J4 — FWD / OFF / REV toggle (JST XH 4-way):** 1 = FWD, 2 = common (0 V), 3 = REV, 4 = 0 V (spare). An
ON-OFF-ON toggle with its common on pin 2.

**J5 — USB-C** (bottom edge, reachable through the slot in the enclosure's end wall). **J6** (SWD: 3V3, SWCLK,
SWDIO, NRST, GND) and **J7** (BOOT0 to 3V3, for the USB DFU bootloader) are footprints for 2.54 mm headers, not fitted.

## Parts and cost

Every part is pinned to a JLCPCB part number in `source/main.tsx` and in the BOM. The list below was checked
against JLCPCB's **live** parts search on 2026-10-14 (the price per part at quantity 5 boards); stock moves daily, so
it says nothing about the day you order.

| Group | Parts (JLCPCB) | Type |
|---|---|---|
| MCU | STM32F072C8T6 (C80488) | extended |
| Power | LMR16006XDDCR (C87080), SWPA4030S220MT 22 µH (C83472), AP2112K-3.3 (C51118), L78L15ABUTR (C81364), NE555DR (C7593), SS210 (C14996), B5819W (C8598), SMBJ28A (C113997), 1206L020/48V PTC (C49318345) | mixed |
| Command | MCP4822-E/SN (C16040), OPA2171AIDR (C40904), DG419DY (C6581), SMAJ15CA (C2848698) | extended |
| Enable / drive OK | BTS4140N (C59442), MMBT3904 (C20526), BAT54 (C22466368), PC817X2 (C66405), 1N4148W (C81598) | mixed |
| Encoder | SP3485EN (C8963) × 2 | basic |
| Display | TM1637 (C5337160), FJ5461BH 0.56 in 4-digit (C38183) | extended |
| Controls | RK09K1130AAU pot (C202373), B3F-4055 (C84931) × 3 | extended |
| Connectors | WJ15EDGRC-3.81-8P (C14235) × 2, B4B-XH-A (C144395) × 2, TYPE-C-31-M-12 (C165948), USBLC6-2SC6 (C7519) | extended |
| Passives | 0402/0603/0805/1206 MLCCs (C1525, C14663, C52923, C15850, C45783, C377773, C13585, C1523, all basic); 0603 5 % RCA resistors (C22369937 etc., extended) | |

**Cost estimate for 5 assembled boards** (JLCPCB, October 2026 prices, before shipping and tax; check the quote):

| Item | Estimate |
|---|---|
| Bare PCBs, 80 × 110 mm, 4 layers, qty 5 | about $15–30 |
| Assembly setup (Standard, needed for the through-hole parts) + stencil | about $25–35 |
| Parts for 5 boards (JLCPCB live prices on 2026-10-15: $73; minimum-order quantities add a little) | about $75–90 |
| Extended-part loading fees: 32 unique extended part numbers × about $3 | about $96 |
| Through-hole soldering (about 60 joints per board) | about $5–10 |
| **Total** | **about $220–260, i.e. about $45–50 per board** |

The biggest saving: 11 of the 32 extended lines are the 0603 resistors. STEVE's catalogue snapshot listed the JLCPCB
*basic* 1 % resistors (for example 10 k C25804, 1 k C21190) as out of stock on the day, so the board uses the RCA 5 %
extended ones. If JLCPCB shows the basic ones in stock when you order, swap them (same 0603 footprint) and save about
$33 in loading fees — and get 1 % parts for the command amplifier's gain resistors (R32–R35), which the firmware
otherwise calibrates out.

Bought separately (not on the PCB order): 22 mm mushroom E-stop with 2 NC contact blocks, ON-OFF-ON toggle with 6 mm
bushing, two 15EDGK-3.81-08P plugs, two JST XHP-4 housings + 8 crimps, M16 × 1.5 cable gland, 6 mm D-shaft knob, eight
M3 × 5.7 heat-set inserts, M3 screws, a 55 × 24 × 1.5 mm clear acrylic window, the pendant cable.

## Ordering (JLCPCB) — the person places the order

STEVE prepares the files; nobody has ordered anything.

1. **Re-check stock first.** The stock STEVE showed is a nightly snapshot of JLCPCB's catalogue (2026-10-14), not
   live assembly stock, and on this day the snapshot was incomplete (it listed most JLCPCB *basic* resistors and
   many ICs as missing). Upload the BOM (STEVE's, or `fabrication/BOM-reference.csv`) on JLCPCB's assembly page: it shows live stock and price for every
   line. Swap anything short for its alternate (table above) and rebuild in STEVE before ordering.
2. **Bare boards:** export `fabrication.zip` from the circuit in STEVE (Electronics → Export, revision 32) and upload it. 4 layers, 1.6 mm, 1 oz outer copper, lead-free
   HASL, green mask, white silkscreen, quantity 5 (JLCPCB's standard 4-layer stackup is fine; no impedance control needed). Check that JLCPCB's render matches STEVE's PCB view.
3. **Assembly:** turn on PCBA, top side, upload the BOM and CPL (pick-and-place) from the same `fabrication.zip`. The
   through-hole parts (J1–J4, display, buttons, knob) need JLCPCB's through-hole assembly option, which Economic
   assembly may not offer for all of them: choose Standard assembly, or leave the THT parts off and solder them by
   hand (they are easy to solder).
   - Check every part's rotation in the placement preview: pin 1 of U1–U11, U13–U15 (U3, the 78L15, could not be checked by STEVE), Q2, Q3, D1, D9, D10;
     the polarity of D2–D5, D11, D14, D15, D6–D8.
   - For this first build choose the paid "confirm parts placement" option.
4. **Prototype first:** 5 boards, test them (below), then order more.
5. Buy separately: the 22 mm E-stop with 2 NC contacts, the ON-OFF-ON toggle, two 8-way 3.81 mm plugs, two JST
   XH 4-way housings and crimps, an M16 × 1.5 cable gland (4.5–10 mm), a 6 mm knob, eight M3 × 5.7 heat-set
   inserts, four M3 × 8 and four M3 × 6 screws, a 55 × 24 × 1.5 mm clear acrylic window.

## Bring-up and test

Do these in order, on a current-limited bench supply (24 V, limit 150 mA), with the drive disconnected first.

1. **Look:** solder bridges on the STM32 (LQFP-48) and the SOICs, the orientation of the diodes and the TVS.
2. **Reverse polarity:** apply −24 V for a few seconds: draw ≤ a few mA (the SS210 blocks), nothing warms.
3. **Power:** +24 V. Idle current about 30–50 mA. Measure: V5 (C6) 4.7–5.0 V, 3.3 V (C9) 3.2–3.4 V, +15 V
   (C11) 14.4–15.6 V, −V (C12) −11 to −13.5 V, the green power LED is on.
4. **Firmware:** fit a jumper on J7 (BOOT0), plug USB-C: the board shows up as "STM32 BOOTLOADER" (DFU). Load the
   test firmware (or the real one) with `dfu-util` or STM32CubeProgrammer, remove the jumper, reset.
5. **Default-off check:** power the board and hold the MCU in reset (short J6 pin 4 NRST to pin 5 GND; a blank
   board behaves the same). J2.1 to J2.2 must read 0 V ± 5 mV (the DG419 connects the terminal to 0 V while CMD_EN
   is low) and J1.3 must read 0 V. Unpowered, the DG419 has no rails and the terminal is not defined: the drive
   must never be enabled without the pendant powered (the enable line is then off as well).
6. **Command:** with the firmware's calibration mode, step the DAC: J2.1 should read −10.0, −5.0, 0.0, +5.0,
   +10.0 V (± 2 % before calibration). Store the gain and offset per direction.
7. **Enable:** RUN with E-stop healthy and J1.5 fed from J1.4 (a wire in place of the drive's fault relay):
   J1.3 = about 23 V. Press STOP: J1.3 drops to 0 V. Open the E-stop monitor: J1.3 drops and the display shows `E-St`.
   Short J1.3 to 0 V for a second: the BTS4140N limits; on release the output comes back.
8. **Encoder:** feed A/B from a function generator through a 26LS31-type driver or connect the drive; check the
   count direction and the rpm against a tachometer.
9. **STO loop:** ohm-meter across J1.6–J1.7: closed with the E-stop released, open when pressed.
10. **With the drive:** set the AKD as above, low speed limit first, then check FWD/REV direction and the ramp.

## Firmware behaviour

Firmware is not written yet; [`firmware/README.md`](firmware/README.md) fixes the pins. The behaviour:

**States**

| State | Entered when | Outputs | Display |
|---|---|---|---|
| `IDLE` | power-up after self-test; STOP; selector moved to OFF; JOG released; ramp finished after STOP | EN_REQ = 0, CMD_EN = 0, DAC A = B = 0 | rpm (0) or `----` without encoder |
| `RUN` | RUN pressed while: E-stop healthy, drive OK, selector FWD or REV, knob below 5 % (no start at speed) | EN_REQ = 1; after 50 ms CMD_EN = 1; command ramps to the knob setting | rpm, RUN LED on |
| `JOG` | JOG held in IDLE with E-stop healthy, drive OK, selector FWD or REV | as RUN, but the target is the jog speed (menu), released = ramp to 0 then IDLE | rpm, RUN LED blinks |
| `FAULT` | drive-OK lost (DRV_OK_N high for > 20 ms) in any state; 24 V below 19 V; DAC/encoder self-test fails | EN_REQ = 0 at once, CMD_EN = 0, DAC = 0 | `Er` + code (`Er 1` drive fault, `Er 2` low 24 V, `Er 3` encoder), FAULT LED on |
| `ESTOP` | ESTOP_N high in any state | EN_REQ = 0 and CMD_EN = 0 at once (hardware already did) | `E-St` flashing, FAULT LED on |

- Leaving `FAULT` / `ESTOP`: the cause must be gone (drive OK, E-stop pulled out), then the operator presses
  STOP to acknowledge; the pendant goes to `IDLE`. It never restarts by itself.
- STOP in `RUN`/`JOG`: drop EN_REQ at once (the hardware also does) — the drive's own stop behaviour (coast or
  ramp, set in the drive) applies; the command ramps to 0 and CMD_EN opens.
- Selector moved while running: treated as STOP. Both FWD and REV low: wiring fault, `Er 4`.
- RUN is a momentary latch: press to start, the state persists until STOP, E-stop, fault or OFF.

**Ramp:** the command moves toward its target at the configured acceleration, in rpm/s converted to DAC codes
through the stored volts-per-rpm, updated every 1 ms. Defaults: 2000 motor rpm/s up, 2000 down. The knob is read
at 1 kHz, filtered (IIR, 50 ms) and has 1 % hysteresis so the command does not hunt. Direction changes always ramp
through 0 V; the other DAC channel stays at 0.

**RPM display:** spindle rpm = (counts in the window / (4 × lines)) × 60 / window / ratio. Window 100 ms,
updated 5 times a second, ±1 rpm resolution above 100 rpm with averaging; shows `----` above 9999.

**Setup menu** (enter: hold STOP and JOG for 3 s in IDLE; knob scrolls, RUN = select/save, STOP = back;
the drive is never enabled in the menu):

| Item | Display | Range / presets | Default |
|---|---|---|---|
| Machine preset | `nAch` | `LAth` 5:1, `nILL` 5:1, `GrNd` 1:1, `SAnd` 5:1, `CSAU` 100:1 (5:1 × 20:1 worm), `bSAU` 25:1 (5:1 × 5:1 belt), `USEr` | `LAth` |
| Lines per motor rev (drive emulation) | `LInE` | 64–8192 | 1024 |
| Extra ratio (user preset) | `rAt` | 0.01–999.99 motor rev per output rev | 5.00 |
| Max speed at full knob | `SPd` | 1–9999 output rpm | machine-dependent |
| Volts per 1000 motor rpm (= AKD AIN.VSCALE) | `uSCL` | 0.1–10.0 | 2.0 |
| Acceleration / deceleration | `ACC` / `dEC` | 10–20000 motor rpm/s | 2000 |
| Jog speed | `JOG` | 1–25 % of max | 5 % |
| Direction invert | `dIr` | on / off | off |
| Count invert | `CntI` | on / off | off |
| Fault input polarity | `FLt` | `oPEn` = fault (relay), `HIGH` = fault | `oPEn` |
| Display brightness | `bri` | 1–7 | 4 |
| DAC calibration | `CAL` | gain and offset per direction, set with a meter on J2 | factory 1.000 / 0 |

Settings are stored in the last two 2 kB flash pages (one copy each, CRC32 and a sequence number). A USB serial
console (CDC) offers the same settings and a status read-out.

## Open issues

1. **Drive interface: check on the real drive.** The wiring table now follows `../hardware/drive-interface.md` (X8.3
   DCOM8 to 0 V for sourcing inputs, X9 pins 1–5). The AKD manual contradicts itself on the fault-relay pins (p. 46
   says X8/9–10, pp. 146 and 161 say X8/1–2): check with a meter before wiring. With a different drive, redo the
   wiring table only (the board is generic).
2. **Not a safety device** (see top). Single-channel STO through one E-stop contact is SIL 2 / PL d at best and only
   if the drive's STO is wired and commissioned per its manual; a risk assessment per machine decides.
3. **Pinouts to verify on the first board** (taken from datasheets, but not seen on a physical part): FJ5461BH
   (common anode, pin 1 = E), TM1637 (TA2007) package pin order, B3F-4055 terminal pairs, RK09K pot (CW/CCW sense:
   swap in firmware if the knob runs backwards), L78L15 in SOT-89 (1 OUT, 2 GND/tab, 3 IN) and its rotation in
   JLCPCB's preview (STEVE could not check it), BTS4140N (SOT-223, IN = 1, OUT = 3).
4. **Stock and prices are not live in STEVE.** The catalogue snapshot (2026-10-14) was incomplete; 15 part numbers
   could not be confirmed there at all. They were in stock on JLCPCB's live search on 2026-10-14, but that says
   nothing about order day: re-check on the BOM upload (Ordering, step 1).
5. **5 % resistors.** The command gain (R32–R35) and the 24 V monitor divider use 5 % parts; the firmware's `CAL`
   step trims command gain and offset per direction. Swap to 1 % basic parts if they are in stock (saves fees too).
6. **Negative rail is unregulated** (about −12.5 V from the NE555 charge pump, varies with load and the 15 V rail).
   The OPA2171 and DG419 only need it to exceed −11 V for a −10 V output: measure it at bring-up (step 3).
7. **Enclosure fit is checked against the board outline and its SMD bodies only.** The linked board brings no 3D
   bodies for the through-hole parts (display, terminal blocks, pot, buttons), so their heights were taken from the
   datasheets: display 8 mm, B3F 7.3 mm, terminal headers about 10 mm, against 13.9 mm of space between the board top and the
   lid. Dry-fit the first print. The flexure buttons, knob hole and display window line up with the board's
   parts by coordinates, not by a checked contact.
8. **Size.** 92 × 165 × 38.5 mm instead of about 90 × 150: the E-stop body (28 × 28 × 33 mm behind the panel) sits
   above the board's top end and the pendant's depth is set by it. A shallower E-stop (one contact layer) or an
   E-stop on a separate housing would bring it to about 150 mm long and 30 mm deep.
9. **Plugs inside the case.** The terminal-block plugs face the bottom end wall; leave 30–40 mm of slack in the cores
   between the gland and the plugs. The USB-C receptacle sits about 17 mm inside the end wall: the slot lines up with
   it, but most cables only reach with a long, slim plug; otherwise program and configure with the lid off (the
   setup menu also works from the pendant's own buttons).
10. **Firmware** is a specification here, not code (see `firmware/README.md`).
11. **Fabrication files.** `fabrication.zip` (Gerbers, drill, BOM, CPL) has to be exported from STEVE by someone
    signed in: the agent tools could only download the board STEP. `fabrication/BOM-reference.csv` is rebuilt from
    the source for the stock check; use STEVE's own BOM and CPL for the order.
12. **Schematic readability.** The schematic is complete and passes the electrical checks but is spread out with long
    wires (one advisory); tidy it with net labels before the design is reused.
13. **Advisories left as they are** (none blocks ordering): 4 copper layers (cost), 17 spots with 0.11–0.125 mm copper
    spacing (JLCPCB limit 0.1 mm), J5's 0.2 mm annular ring, short slots on J5/RV1, parts within 2.5 mm of the board edge
    (Standard assembly may ask for rails), no ESD parts on the unfitted SWD/BOOT headers, and 22 small-capacitor
    footprints that differ slightly from JLCPCB's own (same 0402/0603 package).

## Files

```
pcb/
  README.md                 this file
  source/main.tsx           the STEVE circuit source (tscircuit TSX), revision 32
  source/place.ts           its placement table (board and schematic positions)
  fabrication/              pendant-board.step (the routed board as STEP) and BOM-reference.csv (the BOM rebuilt
                            from the source); export fabrication.zip (Gerbers, drill, BOM, CPL) from STEVE
  firmware/README.md        pin assignments and hardware contract for the firmware
print/pendant/              pendant-tub.stl and pendant-lid.stl, both already in print orientation
```
