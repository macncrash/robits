# Drive interface: Kollmorgen AKD-P00306 (for the control pendant PCB)

The pendant connects to these AKD connectors: **X1** (24 V and STO), **X7** and **X8** (I/O, analog command,
enable, fault relay) and **X9** (encoder emulation output for the RPM readout).

Every pin and rating below comes from the *AKD Installation Manual*, Kollmorgen 903-200003-00, edition AG
(May 2022, hardware revision E/F); page numbers are the printed pages. Parameter names come from the *AKD
User Guide* rev K (2013, firmware 1.10), which is older: check them against the drive's firmware help
(WorkBench) at build time. Kollmorgen's site blocks scripts, so the manuals were read from verbatim mirrors:

- Installation manual: https://www.kml-technology.com/wp-content/uploads/2024/05/Kollmorgen_AKD_Installation_EN.pdf
  (official: https://www.kollmorgen.com/sites/default/files/public_downloads/903-200003-00%20AKD_Installation_en%20Rev%20AG.pdf)
- User guide: https://inmoco.co.uk/wp-content/uploads/2022/01/AKD-Servo-Drive-User-Guide.pdf
- Accessories manual: https://www.raveo.cz/productmanager/wp-content/uploads/2023/02/kollmorgen_accessories_for_digital_drive_systems_akd.pdf

## Summary: what the pendant drives and reads

| Pendant function | AKD pin(s) | Signal type | Setting |
|---|---|---|---|
| Speed command, ±10 V | X8/10 Analog-In+, X8/9 Analog-In−, X8/7 AGND | differential analog | DRV.OPMODE 1, DRV.CMDSOURCE 3, AIN.VSCALE (rpm per volt, motor side) |
| Enable | X8/4 ENABLE (DIGITAL-IN 8), return X8/3 DCOM8 | 24 V digital in | fixed function, active high |
| Fault indication | X8/1 – X8/2 fault relay | dry contact | DOUT.RELAYMODE 0: closed = no fault |
| Fault reset (optional) | X7/3 DIGITAL-IN 4 (or another DIN), return X7/1 DCOM7 | 24 V digital in | DIN4.MODE 1 (fault reset). A rising edge on ENABLE also clears faults by default (DRV.HWENMODE 0) |
| Drive-ready / enabled lamp (optional) | X7/8 DOUT1+, X7/7 DOUT1− | opto output, 24 V 100 mA | DOUT1.MODE 8 (drive enabled) or 11 (drive fault) |
| 24 V for the drive logic | X1/1 +24, X1/2 GND | 24 V ±10 %, 0.5 A | supplied by the cabinet 24 V supply, not by the pendant |
| STO (safe torque off, e-stop) | X1/3 STO, ref X1/2 | 24 V, 45 mA | 24 V present = torque allowed |
| RPM readout | X9/1 A+, X9/2 A−, X9/4 B+, X9/5 B−, X9/7 Z+, X9/8 Z−, X9/3 GND | RS-485 differential (RS-422 compatible) | DRV.EMUEMODE 1, DRV.EMUERES (lines/rev) |

## X1: 24 V supply and STO (3-pole, 3.81 mm pitch; §7.16.5 p. 60, §9.8.3.1 p. 108)

| Pin | Name | Function |
|---|---|---|
| 1 | +24 | +24 Vdc auxiliary supply in, 24 V ±10 %, 0.5 A (no brake) |
| 2 | GND | 24 V return, also the STO reference |
| 3 | STO | STO input: 24 V ±10 %, 45 mA, isolated to 250 Vdc, reaction < 10 ms |

- STO is SIL 2 / PL d, Category 3, **single channel**.
- The drive tolerates OSSD test pulses if they are 300 µs or shorter and 200 ms or more apart (p. 62).
- The drive can only be enabled while STO is at 24 V (p. 155).
- For the pendant, run the e-stop (a positively opening NC contact) in series between +24 V and X1/3.
- Mating plug: Kollmorgen **CON-AKDX1-SL**, supplied with the drive. The 2011 manual named it Phoenix
  **MC 1,5/3-STF-3,81**, which is **not verified** on current hardware.

## X7: digital I/O (10-pole; §9.14.1.1 p. 146)

| Pin | Name | Notes |
|---|---|---|
| 1 | DCOM7 | Common for DIN 1, 2, 3, 4, 7 (pins 10, 9, 4, 3, 2). Tie to 0 V for sourcing (+24 V switched) inputs |
| 2 | DIGITAL-IN 7 | 3.5–30 V on, 2–8 mA |
| 3 | DIGITAL-IN 4 | suggested: fault reset (DIN4.MODE 1) |
| 4 | DIGITAL-IN 3 | suggested: PTC-relay trip, controlled stop (DIN3.MODE 13), if the motor PTC can't go to X10 (see `decisions.md`) |
| 5 | DIGITAL-OUT2− | |
| 6 | DIGITAL-OUT2+ | floating opto output, 30 V / 100 mA max, short-circuit proof |
| 7 | DIGITAL-OUT1− | |
| 8 | DIGITAL-OUT1+ | floating opto output, 30 V / 100 mA max |
| 9 | DIGITAL-IN 2 | fast input, 2–15 mA |
| 10 | DIGITAL-IN 1 | fast input, 2–15 mA |

- The digital outputs need an external 20–30 Vdc I/O supply, applied as the manual shows. Outputs update every
  250 µs.
- Mating plug: **CON-AKDX7-SL** (supplied with the drive). The 2011 manual named it Amphenol **ELXP1010S1**,
  which is **not verified** now.
- Terminals take up to 1.5 mm² (16 AWG), 0.2–0.25 N·m.
- The X7/X8 pitch was not verified. Measure the supplied plug before laying out a board-mounted header.

## X8: fault relay, enable, analog (10-pole; pp. 146–147)

| Pin | Name | Notes |
|---|---|---|
| 1 | Fault relay | Dry contact, 30 Vdc or 42 Vac, 1 A max. Opens or closes in 10 ms or less. 400 Vdc isolation |
| 2 | Fault relay | With DOUT.RELAYMODE 0 (default), the contact is **closed when there is no fault** |
| 3 | DCOM8 | Common for DIN 5, 6, 8 (pins 6, 5, 4). Tie to 0 V for sourcing inputs. Not connected to DCOM7 |
| 4 | **DIGITAL-IN 8 = ENABLE** | Hardware enable, fixed function, active high. 3.5–30 V on, −2 to +2 V off, 2–8 mA. Read directly by the FPGA. In series with the software enable |
| 5 | DIGITAL-IN 6 | 2–8 mA |
| 6 | DIGITAL-IN 5 | 2–8 mA |
| 7 | AGND | Analog ground |
| 8 | Analog-Out | ±10 V, 20 mA, 110 Ω output impedance, 16 bit. Default: actual velocity. Can also drive an analogue RPM meter |
| 9 | **Analog-In−** | |
| 10 | **Analog-In+** | Velocity command. + relative to − turns the motor clockwise; reverse with DRV.DIR |

- **Analog input:** differential, ±12.5 V range, 16 bit, sampled at 16 kHz, input impedance > 13 kΩ, CMRR
  > 30 dB at 60 Hz, offset < 50 mV unadjusted. The maximum is −12.5/+16 V relative to the I/O return.
  - Drive it from the pendant as a true differential pair (for example a ±10 V op-amp output and its
    reference), twisted and shielded, with the shield grounded at the drive end.
  - Null the offset with the drive's analog offset parameter and a deadband (AIN.OFFSET and AIN.DEADBAND,
    not verified on this firmware).
- **Fault contact location:** p. 46 of the same manual says "X8/9–10" for the fault contact, but pp. 146 and
  161 say X8/1–2. Use **X8/1–2**, and check it with a meter on the real drive before the PCB is released.
- Mating plug: **CON-AKDX8-SL** (supplied with the drive; 2011 manual: Amphenol **ELXP1010S2**, not verified).

## X9: encoder emulation output (D-sub 9 **male** on the drive; §9.13.1.3 p. 139, §9.13.5.1 p. 144)

| Pin | Signal (A-quad-B output, DRV.EMUEMODE 1) |
|---|---|
| 1 | A+ |
| 2 | A− |
| 3 | GND |
| 4 | B+ |
| 5 | B− |
| 6 | Shield (capacitively coupled to the drive) |
| 7 | Zero+ (index, once per motor revolution) |
| 8 | Zero− |
| 9 | not connected |

- RS-485 line drivers, with 150 Ω across each pair in the manual's diagram. They work with standard RS-422
  receivers such as the AM26LV32 or SN65LBC175. Terminate each pair at the pendant with 120–150 Ω.
- Maximum output frequency 3 MHz per channel; phase 90° ±20°; maximum cable 100 m.
- **Resolution:** set DRV.EMUERES in lines per motor revolution (0–16,777,215). For an RPM readout, for
  example 1,000 lines/rev gives 4,000 edges/rev. At 3,000 rpm that is 50 kHz on A, well below the limit. The
  output shaft turns at 1/5 of the motor, so the pendant divides the motor rpm by 5 (or set DRV.EMUERES to a
  multiple of 5 and count accordingly).
- The mating D-sub 9 **female** connector is **not** supplied with the drive (p. 32). Use any D-sub 9 female
  with a metal hood.

## Other drive connectors (not on the pendant, for the cabinet wiring)

| Connector | Pins |
|---|---|
| X2 motor (6-pole) | 1 −BR, 2 +BR, 3 PE, 4 U, 5 V, 6 W. KBM lead colours (AKD manual p. 136): U blue, V brown, W violet |
| X3 mains (7-pole, x00306) | 1 −RB, 2 −DC, 3 +DC (+RB), 4 L1, 5 L2, 6 L3, 7 PE. Single-phase 240 V: the manual says to use L1 and N with L3 left open (§9.8.4.2 p. 111). Which terminal takes N: check the manual's diagram on p. 111 (expected L2, not verified) |
| X10 feedback (D-sub 15 HD female) | BiSS-C: 2 CLK+, 3 CLK−, 4 SEN+, 5 SEN−, 6 DAT+, 7 DAT−, 10 +5 V, 11 0 V. Pins 8/9 Th+/Th− (PTC) are listed for incremental, EnDat 2.1, Hiperface and BiSS-B, **not for BiSS-C**. See `decisions.md` |
| X11 | Service Ethernet (RJ45) for WorkBench setup |

## Drive parameters the pendant relies on

| Parameter | Value | Why |
|---|---|---|
| DRV.OPMODE | 1 | Velocity mode |
| DRV.CMDSOURCE | 3 | Analog command |
| AIN.VSCALE | for example 530 rpm/V: 10 V = 5,300 motor rpm, about the 1,060 rpm no-load output speed | Command scaling |
| IL.LIMITP | 5.9 A | Peak current limit from the README (gears sized for 20 N·m) |
| IL.LIMITC / MOTOR.ICONT | 3.0 A (the drive's continuous rating; the motor allows 3.11 A) | Continuous limit |
| MOTOR.RTYPE / MOTOR.TEMPFAULT | 0 (PTC) / trip resistance from the KBM PTC curve | Motor over-temperature, if the PTC is wired to X10 |
| DRV.HWENMODE | 0 | A rising edge on ENABLE clears faults |
| DRV.ENDEFAULT | 1 | The software enable is set at power-up, so the X8/4 switch alone enables the drive |
| DOUT.RELAYMODE | 0 | Fault relay closed = no fault |
| DRV.EMUEMODE / DRV.EMUERES | 1 / for example 1000 | A/B/Z output on X9 |
| FB1.SELECT / FB1.BISSBITS | 34 / 18 (or 17) | AksIM-2 BiSS-C feedback |

Save the settings in the drive's non-volatile memory with DRV.NVSAVE.

## Pendant connector summary

Use two cables, so the low-level analog and RS-422 signals don't run next to the relay and 24 V
wiring:

1. **I/O cable** to X1/X7/X8: 24 V switched for ENABLE and STO; the analog pair (twisted, shielded); fault
   relay pair; optional reset and lamp.
2. **Encoder-emulation cable** to X9: 3 twisted pairs + GND, shielded, D-sub 9 female at the drive.
