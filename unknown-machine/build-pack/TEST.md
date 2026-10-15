# First power-up and acceptance test

Drive: Kollmorgen AKD-P00306 (see [hardware/decisions.md](hardware/decisions.md)), set up with Kollmorgen
WorkBench over Ethernet. Pendant: [pcb/README.md](pcb/README.md). Parameter names below are AKD parameters.
Check each one against the AKD User Guide for your firmware before you rely on it.

**Safety first**
- The drive's bus is about 325 V DC. Wire the cabinet with the mains off, and wait for the bus LED to go out
  before touching X2 or X3.
- Wire the E-stop into STO (X1) from the start. The pendant is not a safety device.
- Bolt the pedestal down before the first spin. Leave the output free (no load, no chuck).

## 1. Before mains

1. **Insulation:** with the motor leads disconnected from the drive, measure each phase to the housing at
   500 V DC. It must read more than 10 MΩ.
2. **Windings:** measure phase to phase on all three pairs. Expect about 6.0 Ω line to line (KBM-17H01-B), the
   same within 3 % on each pair.
3. **Inductance:** measure phase to phase with an LCR meter. The AKD needs at least 2.5 mH at 240 V. If it is
   lower, stop and ask Kollmorgen (a line choke may be needed).
4. **PTC:** measure it cold and compare with the cold resistance on Kollmorgen's PTC curve for the KBM. An open
   circuit or a reading far above the curve means a damaged lead.
5. **By hand:** the output turns smoothly through 5 full turns, with no tight spot. Cogging from the motor is
   normal.

## 2. Drive setup (24 V logic only, mains off)

| Setting | Value | Why |
|---|---|---|
| Motor | KBM-17H01-B from WorkBench's motor list, or entered by hand from the KBM datasheet (poles 10, Kt 0.681 N·m/A, Ke 41.2 Vrms/krpm, R and L as measured) | |
| IL.LIMITP | 5.9 A | Peak torque limit. The gears are sized for 20 N·m: 5.9 A gives 18.3 N·m at the output |
| IL.LIMITC / MOTOR.ICONT | 3.0 A | The drive's continuous rating (the motor's is 3.11 A) |
| MOTOR.RTYPE, MOTOR.TEMPFAULT | PTC, trip per the KBM curve | Only if Kollmorgen confirms the PTC works with BiSS-C; otherwise wire the PTC relay into DIN3 |
| FB1.SELECT | 34 (BiSS-C) | AksIM-2 |
| FB1.BISSBITS | 18 (or 17 for the 17-bit readhead) | Not verified: check the manual |
| VL.LIMITP | 5500 rpm motor (1100 rpm output) | Just above the 1060 rpm no-load speed |
| DRV.OPMODE / DRV.CMDSOURCE | 1 (velocity) / 3 (analog) | Pendant command |
| AIN.VSCALE | 530 rpm/V (motor) | ±10 V = ±5300 rpm motor = ±1060 rpm output |
| DRV.EMUEMODE / DRV.EMUERES | 1 / 1024 lines per motor rev | Encoder output for the pendant's rpm readout |

Save to the drive (DRV.NVSAVE).

## 3. First spin

1. Mains on, drive disabled. Clear faults.
2. Run the commutation alignment (wake and shake). The shaft moves a few degrees.
3. Enable at 0 V command. The output must hold still with no hum.
4. With the pendant at its lowest speed, run 50 rpm at the output in each direction. Check that FWD turns the
   output the way the machine needs (reverse MOTOR.PHASE or the analog sign if not).
5. Step up to 200, 500 and 1000 rpm at the output, about 1 minute each. At each step:
   - the drive's current must stay under about 0.5 A with no load;
   - the noise must be an even gear whine with no knocking once per output turn (a once-per-turn knock
     means a tight spot or a damaged tooth);
   - the pendant's rpm readout must agree with a tachometer within 1 %.
6. Press the E-stop while running at 500 rpm. The drive must report STO, the output must coast to a stop and
   the pendant must show E-STOP. Release it: the drive must NOT restart until RUN is pressed again.

## 4. Run-in and temperature

1. Run 30 minutes at 500 rpm output, no load, then 30 minutes alternating direction every 30 s.
2. Log the housing temperature beside the fins every 5 minutes. With no load it should settle well under
   50 °C. Stop if it passes 70 °C.
3. Drain nothing (the stage is grease-lubricated), but look at the grease at the flange joint: dark metallic
   grease after run-in is normal once; repeat it after re-greasing and it is not.

## 5. Output checks

| Check | How | Target |
|---|---|---|
| Backlash at the output | Lock the motor (drive enabled at zero speed); rock the output with ±2 N·m, read with a dial indicator at a 50 mm radius | Record it. About 0.05–0.15 mm at R50 is expected for grade 6/7 m1 gears with the specified backlash |
| Output runout | Dial on the Ø20 output pilot | under 0.02 mm |
| Torque | Short lever and a spring scale or load cell, motor current at the limit for under 2 s | about 18 N·m at 5.9 A |
| Encoder position | Turn the motor 10 revs by WorkBench jog and compare with a mark | No lost counts |

Record every number on a copy of this page. Together with the gear reports and the CMM reports, these are the
unit's first-article record.
