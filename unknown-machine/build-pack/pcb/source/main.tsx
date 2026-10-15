/**
 * Shop-machine control pendant (24 V, ±10 V speed command, enable, drive-OK, E-stop pass-through, rpm readout)
 *
 * The operator's hand control for the planetary joint actuator family (lathe, mill attachment, bench grinder,
 * disc sander, cold saw, band saw). It drives any servo drive with a ±10 V analog speed input and 24 V I/O;
 * primary target Kollmorgen AKD-P00306 (wiring in build-pack/pcb/README.md).
 *
 * NOT A SAFETY DEVICE. The E-stop's first NC contact is wired straight through this board (J3.1-2 -> J1.6-7)
 * to the drive's STO input with no logic in its path; safety comes from the drive's STO. Everything else here
 * (STOP, enable, ramp to 0 V) is functional control only.
 *
 * Requirements (confirmed):
 * - R1: Drives any ±10 V analog / 24 V I/O servo drive; primary AKD (240 Vac). drive-interface.md did not exist
 *       at schematic time, so the generic interface is used; AKD pins from build-pack/hardware/decisions.md
 *       — an AKD runs from the pendant's command, enable and drive-OK lines
 * - R2: 24 V DC in, reverse-polarity and transient protected, on-board rails — survives a reversed 24 V
 *       supply and a 600 W surge; makes 5.15 V, 3.3 V, +15 V and about -12.5 V
 * - R3: Speed knob, FWD/OFF/REV selector, RUN, STOP, JOG — RUN latches enable through the MCU only with no
 *       fault and a healthy E-stop monitor; STOP pulls the enable driver off in hardware (BAT54), whatever the MCU does
 * - R4: ±10 V bipolar, monotonic, ~2.5 mV steps, ramped in firmware, 0 V when not running — DG419 switch
 *       rests on 0 V and only the running MCU switches it to the amplifier; enable and switch drop on MCU reset (pull-downs)
 * - R5: Enable: sourcing 24 V, short-circuit protected (BTS4140N); drive-OK input: 24 V through a PC817 opto
 * - R6: 22 mm E-stop, two NC contacts: #1 straight through to STO (0.5 mm copper, no logic), #2 read by the
 *       MCU (ESTOP_N) and also forces the enable driver off in hardware (Q3)
 * - R7: Encoder emulation A/B RS-422 (5 V) -> 2 × SP3485 receivers -> STM32 TIM2 encoder mode; 4-digit 0.56 in
 *       LED (TM1637) shows rpm; lines/rev and ratio (5:1, 5:1, 20:1, 1:1) set in a menu, stored in flash
 * - R8: STM32F072C8T6 (64 KB flash, crystal-less USB); USB-C (ROM DFU bootloader via BOOT0) and an SWD header
 * - R9: Two 8-way pluggable 3.81 mm terminal blocks + USB-C, all on the bottom edge (cable gland end)
 * - R10: 80 × 110 mm board for a ~90 × 160 mm hand-held pendant; display, knob and buttons on top; E-stop
 *        and toggle selector are panel parts in the lid, wired to J3 / J4
 * - R11: 5 prototypes, JLCPCB PCB + assembly
 *
 * Key decisions:
 * - Power: 24 V -> PTC (200 mA, 48 V) -> SMBJ28A TVS -> SS210 reverse diode -> V24.
 *   V24 -> LMR16006X buck (60 V) -> 5.15 V -> Schottky OR with USB VBUS -> V5 -> AP2112K -> V3_3.
 *   V24 -> 78L15 -> +15 V; NE555 astable + diode charge pump -> about -12.5 V; both for the output stage only.
 * - Command: MCP4822 dual 12-bit DAC (internal 2.048 V ref). OPA2171 (36 V, rail-to-rail out) difference amp: CMD = 5.1 × (A − B):
 *   A forward, B reverse, both 0 at power-up = 0 V. ±10.4 V full scale, ~2.5 mV/step; firmware trims gain/offset.
 * - Enable: EN_REQ -> Q2 -> BTS4140N (60 V protected high-side switch, IN pulled low = on).
 * - Drive OK: the AKD fault relay is a dry contact (closed = OK). J1.4 sources V24 to it; its return J1.5 lights
 *   the PC817, so DRV_OK_N low = drive OK and a broken wire reads as a fault.
 * - MCU: STM32F072C8T6 in LQFP-48 instead of the RP2040 first drawn: internal flash and crystal-less USB remove the QSPI
 *   flash, crystal and 1.1 V rail, its 5 V-tolerant open-drain pins drive the TM1637 without level shifters, and the
 *   0.5 mm gull-wing package routes cleanly where the RP2040's 0.4 mm QFN did not.
 * - Board: 80 x 110 mm, 4 layers (the autorouter needs the inner layers to keep every power and ground trace at
 *   0.3 mm or more), every trace at least 0.3 mm, 0.3/0.6 mm vias.
 * - Resistors are 5 % RCA0603 parts because the parts snapshot showed the 1 % basic ones out of stock (see README).
 *
 * Pinouts taken from datasheets: DG419 (Vishay SOIC-8), L78L15 SOT-89 (1 OUT, 2 GND, 3 IN), NE555, STM32F072 (DS9826 table 13), TM1637 V2.4,
 * MCP4822, OPA2171, SP3485, PC817, BTS4140N (IN=1, VBB=2/4, OUT=3), FJ5461BH (common anode). Open questions:
 * build-pack/pcb/README.md.
 */
import { P, HOLES, SILK } from "./place"

const at = (n: string, defSr?: number) => {
  const [x, y, r = 0, sx = 0, sy = 0, sr] = P[n]
  const o: any = { pcbX: x, pcbY: y, pcbRotation: r, schX: sx, schY: sy }
  if (sr !== undefined) o.schRotation = sr
  else if (defSr !== undefined) o.schRotation = defSr
  return o
}
const RES: Record<string, [string, string, string]> = {
  "10k": ["10k", "C22369937", "0603"], "1k": ["1k", "C22356624", "0603"], "5k1": ["5.1k", "C22356620", "0603"],
  "100k": ["100k", "C22356636", "0603"], "4k7": ["4.7k", "C22356632", "0603"], "22": ["22", "C22356629", "0603"],
  "47k": ["47k", "C22356630", "0603"], "8k2": ["8.2k", "C22356668", "0603"], "51k": ["51k", "C22369960", "0603"],
  "120": ["120", "C22369939", "0603"], "10k0805": ["10k", "C49196820", "0805"],
}
const CAP: Record<string, [string, string, string, string]> = {
  "100n": ["100nF", "C1525", "0402", "16V"], "100n50": ["100nF", "C14663", "0603", "50V"], "1u": ["1uF", "C52923", "0402", "25V"],
  "10u": ["10uF", "C15850", "0805", "25V"], "22u": ["22uF", "C45783", "0805", "25V"], "2u2": ["2.2uF", "C377773", "0805", "50V"],
  "10u50": ["10uF", "C13585", "1206", "50V"], "33p": ["33pF", "C5137486", "0402", "50V"], "1n": ["1nF", "C1523", "0402", "50V"],
}
const R = ({ n, v, a, b }: any) => (
  <resistor name={n} resistance={RES[v][0]} footprint={RES[v][2]} supplierPartNumbers={{ jlcpcb: [RES[v][1]] }} {...at(n, 270)}
    connections={{ pin1: `net.${a}`, pin2: `net.${b}` }} />
)
const C = ({ n, v, a, b }: any) => (
  <capacitor name={n} capacitance={CAP[v][0]} footprint={CAP[v][2]} maxVoltageRating={CAP[v][3]} supplierPartNumbers={{ jlcpcb: [CAP[v][1]] }}
    {...at(n, 270)} connections={{ pin1: `net.${a}`, pin2: `net.${b}` }} />
)
// pins: labels in pad order (pin1, pin2, ...); conn: label -> net; dnc: labels left open; arr: schPinArrangement
const U = ({ n, c, mpn, pins, conn, pwr = [], gnd = [], dnc = [], must = [], provides = {}, arr, tag = "chip" }: any) => {
  const pinLabels: any = {}
  pins.forEach((l: string, i: number) => { pinLabels[`pin${i + 1}`] = l })
  const pinAttributes: any = {}
  pwr.forEach((l: string) => (pinAttributes[l] = { requiresPower: true }))
  gnd.forEach((l: string) => (pinAttributes[l] = { requiresGround: true }))
  dnc.forEach((l: string) => (pinAttributes[l] = { doNotConnect: true }))
  must.forEach((l: string) => (pinAttributes[l] = { mustBeConnected: true }))
  Object.entries(provides).forEach(([l, v]) => (pinAttributes[l] = { providesPower: true, providesVoltage: v }))
  const connections: any = {}
  Object.entries(conn).forEach(([l, net]) => (connections[l] = `net.${net}`))
  const props: any = { name: n, footprint: `jlcpcb:${c}`, supplierPartNumbers: { jlcpcb: [c] }, manufacturerPartNumber: mpn, ...at(n),
    pinLabels, connections }
  if (Object.keys(pinAttributes).length) props.pinAttributes = pinAttributes
  if (arr) props.schPinArrangement = arr
  return tag === "connector" ? <connector {...props} /> : <chip {...props} />
}
const S = (pins: string[], d = "top-to-bottom") => ({ direction: d, pins })
const D = ({ n, c, mpn, anode, cathode }: any) => (
  <diode name={n} footprint={`jlcpcb:${c}`} supplierPartNumbers={{ jlcpcb: [c] }} manufacturerPartNumber={mpn}
    pinLabels={{ pin1: "cathode", pin2: "anode" }} {...at(n, 0)} connections={{ anode: `net.${anode}`, cathode: `net.${cathode}` }} />
)
const LED = ({ n, color, fp, c, mpn, anode }: any) => (
  <led name={n} color={color} footprint={fp} supplierPartNumbers={{ jlcpcb: [c] }} manufacturerPartNumber={mpn} {...at(n, 0)}
    connections={{ anode: `net.${anode}`, cathode: "net.GND" }} />
)

// STM32F072C8T6, LQFP-48, pins 1..48 (datasheet DS9826 table 13)
const MCU_PINS = ["VBAT", "PC13", "PC14", "PC15", "PF0", "PF1", "NRST", "VSSA", "VDDA", "PA0", "PA1", "PA2", "PA3", "PA4", "PA5", "PA6",
  "PA7", "PB0", "PB1", "PB2", "PB10", "PB11", "VSS1", "VDD1", "PB12", "PB13", "PB14", "PB15", "PA8", "PA9", "PA10", "PA11", "PA12", "PA13",
  "VSS2", "VDDIO2", "PA14", "PA15", "PB3", "PB4", "PB5", "PB6", "PB7", "BOOT0", "PB8", "PB9", "VSS3", "VDD2"]
const MCU_UNUSED = ["PC13", "PC14", "PC15", "PF0", "PF1", "PA6", "PB2", "PB10", "PB11", "PA15", "PB5", "PB8", "PB9"]
const MCU_CONN = {
  VBAT: "V3_3", VDDA: "V3_3", VDD1: "V3_3", VDD2: "V3_3", VDDIO2: "V3_3", VSSA: "GND", VSS1: "GND", VSS2: "GND", VSS3: "GND",
  NRST: "NRST", BOOT0: "BOOT0", PA13: "SWDIO", PA14: "SWCLK", PA11: "USB_DM_MCU", PA12: "USB_DP_MCU",
  PA0: "ENC_A", PA1: "ENC_B", PA2: "ADC_POT", PA3: "ADC_V24", PA4: "DAC_CS", PA5: "DAC_SCK", PA7: "DAC_SDI",
  PB0: "CMD_EN", PB1: "EN_REQ", PB12: "DRV_OK_N", PB13: "ESTOP_N", PB14: "STOP_N", PB15: "RUN_N",
  PA8: "JOG_N", PA9: "FWD_N", PA10: "REV_N", PB3: "LED_RUN", PB4: "LED_FLT", PB6: "TM_CLK", PB7: "TM_DIO",
}

// Widths for the design currents: 24 V input < 0.2 A, 5 V < 0.15 A, 3.3 V < 0.1 A, +/-15 V < 10 mA, STO loop 45 mA, enable < 20 mA
const POWER_NETS: [string, string][] = [["V24_IN", "0.5mm"], ["V24_F", "0.5mm"], ["V24", "0.5mm"], ["V5_BUCK", "0.5mm"], ["V5", "0.5mm"],
  ["VBUS", "0.5mm"], ["V3_3", "0.5mm"], ["V15P", "0.5mm"], ["V15N", "0.5mm"], ["BUCK_SW", "0.5mm"],
  ["BUCK_CB", "0.3mm"], ["BUCK_FB", "0.3mm"], ["STO_A", "0.5mm"], ["STO_B", "0.5mm"], ["EN_OUT", "0.5mm"], ["PUMP_DRV", "0.5mm"],
  ["PUMP_N", "0.5mm"]]

export default () => (
  <board width="80mm" height="110mm" borderRadius="3mm" thickness="1.6mm" layers={4} minTraceToPadEdgeClearance="0.1mm" minTraceWidth="0.3mm"
    pcbStyle={{ viaHoleDiameter: "0.3mm", viaPadDiameter: "0.6mm", silkscreenFontSize: "1mm" }}>
    {/* Net widths for routing; every other net routes at signal width */}
    {POWER_NETS.map(([n, w]) => <net name={n} nominalTraceWidth={w} />)}
    <net name="GND" nominalTraceWidth="0.5mm" />
    <net name="ADC_V24" nominalTraceWidth="0.3mm" />
    {HOLES.map(([x, y]) => <hole diameter="3.2mm" pcbX={x} pcbY={y} />)}

    {/* Cable terminals (bottom edge), E-stop harness, selector harness */}
    <U n="J1" c="C14235" mpn="WJ15EDGRC-3.81-8P" pins={["V24_IN", "GND1", "EN_OUT", "FLT_SRC", "FLT_IN", "STO_A", "STO_B", "GND2"]}
      conn={{ V24_IN: "V24_IN", GND1: "GND", EN_OUT: "EN_OUT", FLT_SRC: "V24", FLT_IN: "FLT_IN", STO_A: "STO_A", STO_B: "STO_B", GND2: "GND" }}
      arr={{ rightSide: S(["V24_IN", "GND1", "EN_OUT", "FLT_SRC", "FLT_IN", "STO_A", "STO_B", "GND2"]) }} />
    <U n="J2" c="C14235" mpn="WJ15EDGRC-3.81-8P" pins={["CMD", "AGND", "A_P", "A_N", "B_P", "B_N", "ENC_0V", "SHLD"]}
      conn={{ CMD: "CMD_OUT", AGND: "GND", A_P: "ENC_A_P", A_N: "ENC_A_N", B_P: "ENC_B_P", B_N: "ENC_B_N", ENC_0V: "GND", SHLD: "GND" }}
      arr={{ rightSide: S(["CMD", "AGND", "A_P", "A_N", "B_P", "B_N", "ENC_0V", "SHLD"]) }} />
    <U n="J3" c="C144395" mpn="B4B-XH-A(LF)(SN)" pins={["STO_A", "STO_B", "MON", "MON_0V"]}
      conn={{ STO_A: "STO_A", STO_B: "STO_B", MON: "ESTOP_N", MON_0V: "GND" }} arr={{ rightSide: S(["STO_A", "STO_B", "MON", "MON_0V"]) }} />
    <U n="J4" c="C144395" mpn="B4B-XH-A(LF)(SN)" pins={["FWD", "COM", "REV", "COM2"]}
      conn={{ FWD: "FWD_N", COM: "GND", REV: "REV_N", COM2: "GND" }} arr={{ rightSide: S(["FWD", "COM", "REV", "COM2"]) }} />

    {/* 24 V input: PTC, TVS, reverse-polarity Schottky */}
    <fuse name="F1" currentRating="0.2A" footprint="1206" supplierPartNumbers={{ jlcpcb: ["C49318345"] }} manufacturerPartNumber="1206L020/48V"
      {...at("F1")} connections={{ pin1: "net.V24_IN", pin2: "net.V24_F" }} />
    <U n="D1" c="C113997" mpn="SMBJ28A" pins={["C", "A"]} conn={{ C: "V24_F", A: "GND" }}
      arr={{ topSide: S(["C"], "left-to-right"), bottomSide: S(["A"], "left-to-right") }} />
    <D n="D2" c="C14996" mpn="SS210" anode="V24_F" cathode="V24" />
    <C n="C1" v="10u50" a="V24" b="GND" />
    <C n="C2" v="100n50" a="V24" b="GND" />

    {/* 5 V buck: LMR16006X (4-60 V in), FB 47k/8.2k -> 5.15 V */}
    <U n="U1" c="C87080" mpn="LMR16006XDDCR" pins={["CB", "GND", "FB", "EN", "VIN", "SW"]}
      conn={{ VIN: "V24", EN: "V24", GND: "GND", CB: "BUCK_CB", SW: "BUCK_SW", FB: "BUCK_FB" }} pwr={["VIN"]} gnd={["GND"]} must={["EN"]}
      arr={{ leftSide: S(["VIN", "EN"]), rightSide: S(["CB", "SW", "FB"]), bottomSide: S(["GND"], "left-to-right") }} />
    <C n="C3" v="2u2" a="V24" b="GND" />
    <C n="C4" v="100n" a="BUCK_CB" b="BUCK_SW" />
    <inductor name="L1" inductance="22uH" footprint="jlcpcb:C83472" supplierPartNumbers={{ jlcpcb: ["C83472"] }} manufacturerPartNumber="SWPA4030S220MT"
      {...at("L1")} connections={{ pin1: "net.BUCK_SW", pin2: "net.V5_BUCK" }} />
    <D n="D3" c="C14996" mpn="SS210" anode="GND" cathode="BUCK_SW" />
    <R n="R1" v="47k" a="V5_BUCK" b="BUCK_FB" />
    <R n="R2" v="8k2" a="BUCK_FB" b="GND" />
    <C n="C5" v="22u" a="V5_BUCK" b="GND" />
    <D n="D4" c="C8598" mpn="B5819W SL" anode="V5_BUCK" cathode="V5" />
    <D n="D5" c="C8598" mpn="B5819W SL" anode="VBUS" cathode="V5" />
    <C n="C6" v="10u" a="V5" b="GND" />

    {/* 3.3 V LDO and power LED */}
    <U n="U2" c="C51118" mpn="AP2112K-3.3TRG1" pins={["VIN", "GND", "EN", "NC", "VOUT"]} conn={{ VIN: "V5", EN: "V5", GND: "GND", VOUT: "V3_3" }}
      pwr={["VIN"]} gnd={["GND"]} dnc={["NC"]} provides={{ VOUT: 3.3 }}
      arr={{ leftSide: S(["VIN", "EN"]), rightSide: S(["VOUT", "NC"]), bottomSide: S(["GND"], "left-to-right") }} />
    <C n="C7" v="1u" a="V5" b="GND" />
    <C n="C8" v="1u" a="V3_3" b="GND" />
    <C n="C9" v="10u" a="V3_3" b="GND" />
    <R n="R3" v="1k" a="V3_3" b="LED_PWR_A" />
    <LED n="D6" color="green" fp="led0805" c="C2297" mpn="KT-0805G" anode="LED_PWR_A" />

    {/* Output-stage rails: +15 V from a 78L15 (V15P); about -12.5 V (V15N) from an NE555 astable (~70 kHz,
        1k / 10k / 1 nF) driving a diode charge pump - the classic NE555 negative-supply circuit. Loads: OPA2171 + DG419, < 5 mA. */}
    <U n="U3" c="C81364" mpn="L78L15ABUTR" pins={["OUT", "GND", "IN"]} conn={{ IN: "V24", GND: "GND", OUT: "V15P" }}
      pwr={["IN"]} gnd={["GND"]} provides={{ OUT: 15 }}
      arr={{ leftSide: S(["IN"]), rightSide: S(["OUT"]), bottomSide: S(["GND"], "left-to-right") }} />
    <C n="C10" v="2u2" a="V24" b="GND" />
    <C n="C11" v="2u2" a="V15P" b="GND" />
    <U n="U14" c="C7593" mpn="NE555DR" pins={["GND", "TRIG", "OUT", "RESET", "CTRL", "THRES", "DISCH", "VCC"]}
      conn={{ GND: "GND", TRIG: "OSC_C", OUT: "PUMP_DRV", RESET: "V15P", CTRL: "OSC_CTRL", THRES: "OSC_C", DISCH: "OSC_D", VCC: "V15P" }}
      pwr={["VCC"]} gnd={["GND"]} must={["RESET"]}
      arr={{ leftSide: S(["RESET", "CTRL", "THRES", "TRIG"]), rightSide: S(["VCC", "OUT", "DISCH", "GND"]) }} />
    <C n="C53" v="100n50" a="V15P" b="GND" />
    <R n="R40" v="1k" a="V15P" b="OSC_D" />
    <R n="R41" v="10k" a="OSC_D" b="OSC_C" />
    <C n="C51" v="1n" a="OSC_C" b="GND" />
    <C n="C52" v="100n" a="OSC_CTRL" b="GND" />
    <C n="C54" v="10u" a="PUMP_DRV" b="PUMP_N" />
    <D n="D14" c="C8598" mpn="B5819W SL" anode="PUMP_N" cathode="GND" />
    <D n="D15" c="C8598" mpn="B5819W SL" anode="V15N" cathode="PUMP_N" />
    <C n="C12" v="10u" a="V15N" b="GND" />
    <R n="R38" v="100k" a="V24" b="ADC_V24" />
    <R n="R39" v="10k" a="ADC_V24" b="GND" />
    <C n="C49" v="100n" a="ADC_V24" b="GND" />

    {/* STM32F072C8T6: 3.3 V, internal 48 MHz RC trimmed from USB SOF (crystal-less USB), ROM DFU bootloader when BOOT0 is high */}
    <U n="U11" c="C80488" mpn="STM32F072C8T6" pins={MCU_PINS} conn={MCU_CONN}
      pwr={["VBAT", "VDDA", "VDD1", "VDD2", "VDDIO2"]} gnd={["VSSA", "VSS1", "VSS2", "VSS3"]} dnc={MCU_UNUSED} must={["NRST", "BOOT0"]}
      arr={{ leftSide: S(["VBAT", "VDDA", "VDD1", "VDD2", "VDDIO2", "NRST", "BOOT0", "PA13", "PA14", "PA11", "PA12", "VSSA", "VSS1", "VSS2", "VSS3"]),
        rightSide: S(["PB6", "PB7", "PA5", "PA7", "PA4", "PB0", "PB1", "PB12", "PB13", "PB14", "PB15", "PA8", "PA9", "PA10", "PA0", "PA1",
          "PB3", "PB4", "PA2", "PA3", ...MCU_UNUSED]) }} />
    {["C20", "C21", "C22", "C23", "C24"].map((n) => <C n={n} v="100n" a="V3_3" b="GND" />)}
    <C n="C28" v="1u" a="V3_3" b="GND" />
    <C n="C34" v="10u" a="V3_3" b="GND" />
    <C n="C25" v="100n" a="NRST" b="GND" />
    <R n="R6" v="10k" a="BOOT0" b="GND" />
    <pinheader name="J7" pinCount={2} pitch="2.54mm" doNotPlace pinLabels={["BOOT0", "V3_3"]} {...at("J7")} schFacingDirection="left"
      connections={{ BOOT0: "net.BOOT0", V3_3: "net.V3_3" }} />
    <pinheader name="J6" pinCount={5} pitch="2.54mm" doNotPlace pinLabels={["V3_3", "SWCLK", "SWDIO", "NRST", "GND"]} {...at("J6")}
      schFacingDirection="right" connections={{ V3_3: "net.V3_3", SWCLK: "net.SWCLK", SWDIO: "net.SWDIO", NRST: "net.NRST", GND: "net.GND" }} />

    {/* USB-C (configuration and firmware) */}
    <connector name="J5" footprint="jlcpcb:C165948" supplierPartNumbers={{ jlcpcb: ["C165948"] }} manufacturerPartNumber="TYPE-C-31-M-12" {...at("J5")}
      connections={{ VBUS1: "net.VBUS", VBUS2: "net.VBUS", GND1: "net.GND", GND2: "net.GND", EH1: "net.GND", EH2: "net.GND", EH3: "net.GND",
        EH4: "net.GND", DP1: "net.USB_DP", DP2: "net.USB_DP", DN1: "net.USB_DM", DN2: "net.USB_DM", CC1: "net.CC1", CC2: "net.CC2" }} />
    <R n="R8" v="5k1" a="CC1" b="GND" />
    <R n="R9" v="5k1" a="CC2" b="GND" />
    <U n="U13" c="C7519" mpn="USBLC6-2SC6" pins={["IO1A", "GND", "IO2A", "IO2B", "VBUS", "IO1B"]}
      conn={{ IO1A: "USB_DP", IO1B: "USB_DP", IO2A: "USB_DM", IO2B: "USB_DM", GND: "GND", VBUS: "VBUS" }} pwr={["VBUS"]} gnd={["GND"]} />
    <C n="C50" v="100n" a="VBUS" b="GND" />
    <R n="R10" v="22" a="USB_DP" b="USB_DP_MCU" />
    <R n="R11" v="22" a="USB_DM" b="USB_DM_MCU" />

    {/* Display: TM1637 (5 V) drives the 4-digit 0.56 in common-anode LED; the MCU's 5 V-tolerant open-drain pins (PB6/PB7) talk to it directly */}
    <U n="U10" c="C5337160" mpn="TM1637(TA2007)"
      pins={["GND", "SEG1", "SEG2", "SEG3", "SEG4", "SEG5", "SEG6", "SEG7", "SEG8", "GRID6", "GRID5", "GRID4", "GRID3", "GRID2", "GRID1", "VDD", "DIO", "CLK", "K1", "K2"]}
      conn={{ GND: "GND", VDD: "V5", DIO: "TM_DIO", CLK: "TM_CLK", SEG1: "SEG_A", SEG2: "SEG_B", SEG3: "SEG_C", SEG4: "SEG_D", SEG5: "SEG_E",
        SEG6: "SEG_F", SEG7: "SEG_G", SEG8: "SEG_DP", GRID1: "DIG1", GRID2: "DIG2", GRID3: "DIG3", GRID4: "DIG4" }}
      pwr={["VDD"]} gnd={["GND"]} dnc={["GRID5", "GRID6", "K1", "K2"]}
      arr={{ leftSide: S(["VDD", "CLK", "DIO", "K1", "K2", "GND"]),
        rightSide: S(["SEG1", "SEG2", "SEG3", "SEG4", "SEG5", "SEG6", "SEG7", "SEG8", "GRID1", "GRID2", "GRID3", "GRID4", "GRID5", "GRID6"]) }} />
    <C n="C40" v="100n" a="V5" b="GND" />
    <C n="C41" v="10u" a="V5" b="GND" />
    <U n="DS1" c="C38183" mpn="FJ5461BH" pins={["E", "D", "DP", "C", "G", "DIG4", "B", "DIG3", "DIG2", "F", "A", "DIG1"]}
      conn={{ A: "SEG_A", B: "SEG_B", C: "SEG_C", D: "SEG_D", E: "SEG_E", F: "SEG_F", G: "SEG_G", DP: "SEG_DP", DIG1: "DIG1", DIG2: "DIG2", DIG3: "DIG3", DIG4: "DIG4" }}
      arr={{ leftSide: S(["A", "B", "C", "D", "E", "F", "G", "DP", "DIG1", "DIG2", "DIG3", "DIG4"]) }} />
    <R n="R14" v="10k" a="V5" b="TM_CLK" />
    <R n="R15" v="10k" a="V5" b="TM_DIO" />
    <R n="R16" v="1k" a="LED_RUN" b="LED_RUN_A" />
    <LED n="D7" color="green" fp="led0805" c="C2297" mpn="KT-0805G" anode="LED_RUN_A" />
    <R n="R17" v="1k" a="LED_FLT" b="LED_FLT_A" />
    <LED n="D8" color="red" fp="led0603" c="C2286" mpn="KT-0603R" anode="LED_FLT_A" />

    {/* Operator controls: speed knob, RUN / STOP / JOG; pull-ups for buttons, selector and E-stop monitor */}
    <U n="RV1" c="C202373" mpn="RK09K1130AAU" pins={["CCW", "WIPER", "CW", "LUG1", "LUG2"]}
      conn={{ CCW: "GND", WIPER: "POT_W", CW: "V3_3", LUG1: "GND", LUG2: "GND" }} />
    <R n="R18" v="1k" a="POT_W" b="ADC_POT" />
    <C n="C42" v="100n" a="ADC_POT" b="GND" />
    {[["SW1", "RUN_N"], ["SW2", "STOP_N"], ["SW3", "JOG_N"]].map(([n, net]) => (
      <U n={n} c="C84931" mpn="B3F-4055" pins={["T1", "T2", "T3", "T4"]} conn={{ T1: net, T4: "GND" }} dnc={["T2", "T3"]}
        arr={{ leftSide: S(["T1", "T2"]), rightSide: S(["T4", "T3"]) }} />
    ))}
    <R n="R19" v="10k" a="V3_3" b="RUN_N" />
    <R n="R20" v="10k" a="V3_3" b="STOP_N" />
    <R n="R21" v="10k" a="V3_3" b="JOG_N" />
    <R n="R22" v="10k" a="V3_3" b="FWD_N" />
    <R n="R23" v="10k" a="V3_3" b="REV_N" />
    <R n="R24" v="10k" a="V3_3" b="ESTOP_N" />
    <C n="C43" v="100n" a="ESTOP_N" b="GND" />

    {/* Enable output. STOP (via BAT54 D9) and an open E-stop monitor (via Q3) hold Q2 off in hardware. */}
    <R n="R25" v="4k7" a="EN_REQ" b="EN_BASE" />
    <R n="R26" v="100k" a="EN_BASE" b="GND" />
    <U n="Q2" c="C20526" mpn="MMBT3904" pins={["B", "E", "C"]} conn={{ B: "EN_BASE", E: "GND", C: "BTS_IN" }}
      arr={{ leftSide: S(["B"]), topSide: S(["C"], "left-to-right"), bottomSide: S(["E"], "left-to-right") }} />
    <U n="D9" c="C22466368" mpn="BAT54" pins={["A", "NC", "K"]} conn={{ A: "EN_BASE", K: "STOP_N" }} dnc={["NC"]}
      arr={{ leftSide: S(["A"]), rightSide: S(["K", "NC"]) }} />
    <R n="R27" v="10k" a="ESTOP_N" b="ESTOP_B" />
    <U n="Q3" c="C20526" mpn="MMBT3904" pins={["B", "E", "C"]} conn={{ B: "ESTOP_B", E: "GND", C: "EN_BASE" }}
      arr={{ leftSide: S(["B"]), topSide: S(["C"], "left-to-right"), bottomSide: S(["E"], "left-to-right") }} />
    <U n="U6" c="C59442" mpn="BTS4140N" pins={["IN", "VBB", "OUT", "VBB_TAB"]} conn={{ IN: "BTS_IN", VBB: "V24", VBB_TAB: "V24", OUT: "EN_OUT" }}
      pwr={["VBB", "VBB_TAB"]} arr={{ leftSide: S(["IN"]), topSide: S(["VBB", "VBB_TAB"], "left-to-right"), rightSide: S(["OUT"]) }} />
    <U n="D10" c="C113997" mpn="SMBJ28A" pins={["C", "A"]} conn={{ C: "EN_OUT", A: "GND" }}
      arr={{ topSide: S(["C"], "left-to-right"), bottomSide: S(["A"], "left-to-right") }} />

    {/* Drive-OK input: AKD fault relay (closed = OK) lights the PC817 */}
    <R n="R28" v="10k0805" a="FLT_IN" b="OPTO_A" />
    <D n="D11" c="C81598" mpn="1N4148W" anode="GND" cathode="OPTO_A" />
    <U n="U7" c="C66405" mpn="PC817X2CSP9F" pins={["A", "K", "E", "C"]} conn={{ A: "OPTO_A", K: "GND", E: "GND", C: "DRV_OK_N" }}
      arr={{ leftSide: S(["A", "K"]), rightSide: S(["C", "E"]) }} />
    <R n="R29" v="10k" a="V3_3" b="DRV_OK_N" />

    {/* Encoder emulation receivers (RS-422 A/B, 120 ohm terminated) */}
    {[["U8", "C44", "R30", "ENC_A", "ENC_A_P", "ENC_A_N"], ["U9", "C45", "R31", "ENC_B", "ENC_B_P", "ENC_B_N"]].map(([u, cc, rr, ro, ap, an]) => (
      <>
        <U n={u} c="C8963" mpn="SP3485EN-L/TR" pins={["RO", "RE", "DE", "DI", "GND", "A", "B", "VCC"]}
          conn={{ RO: ro, RE: "GND", DE: "GND", DI: "GND", GND: "GND", A: ap, B: an, VCC: "V3_3" }} pwr={["VCC"]} gnd={["GND"]}
          arr={{ leftSide: S(["A", "B"]), rightSide: S(["RO", "RE", "DE", "DI"]), topSide: S(["VCC"], "left-to-right"), bottomSide: S(["GND"], "left-to-right") }} />
        <R n={rr} v="120" a={ap} b={an} />
        <C n={cc} v="100n" a="V3_3" b="GND" />
      </>
    ))}

    {/* Speed command: MCP4822 -> OPA2171 difference amp, CMD = 5.1 x (A - B) -> DG419 (rests on 0 V; MCU switches it while running) */}
    <U n="U4" c="C16040" mpn="MCP4822-E/SN" pins={["VDD", "CS", "SCK", "SDI", "LDAC", "VOUTB", "VSS", "VOUTA"]}
      conn={{ VDD: "V3_3", CS: "DAC_CS", SCK: "DAC_SCK", SDI: "DAC_SDI", LDAC: "GND", VOUTB: "DAC_B", VSS: "GND", VOUTA: "DAC_A" }}
      pwr={["VDD"]} gnd={["VSS"]} must={["LDAC"]}
      arr={{ leftSide: S(["CS", "SCK", "SDI", "LDAC"]), rightSide: S(["VOUTA", "VOUTB"]), topSide: S(["VDD"], "left-to-right"), bottomSide: S(["VSS"], "left-to-right") }} />
    <C n="C46" v="100n" a="V3_3" b="GND" />
    <R n="R32" v="10k" a="DAC_A" b="OPA_INP" />
    <R n="R33" v="51k" a="OPA_INP" b="GND" />
    <R n="R34" v="10k" a="DAC_B" b="OPA_INN" />
    <R n="R35" v="51k" a="OPA_INN" b="OPA_OUT" />
    <U n="U5" c="C40904" mpn="OPA2171AIDR" pins={["OUT1", "IN1N", "IN1P", "VNEG", "IN2P", "IN2N", "OUT2", "VPOS"]}
      conn={{ OUT1: "OPA_OUT", IN1N: "OPA_INN", IN1P: "OPA_INP", VNEG: "V15N", IN2P: "GND", IN2N: "OPB_FB", OUT2: "OPB_FB", VPOS: "V15P" }}
      pwr={["VPOS", "VNEG"]}
      arr={{ leftSide: S(["IN1P", "IN1N", "IN2P", "IN2N"]), rightSide: S(["OUT1", "OUT2"]), topSide: S(["VPOS"], "left-to-right"), bottomSide: S(["VNEG"], "left-to-right") }} />
    <C n="C47" v="100n50" a="V15P" b="GND" />
    <C n="C48" v="100n50" a="V15N" b="GND" />
    <R n="R36" v="22" a="OPA_OUT" b="CMD_PRE" />
    {/* DG419 SPDT analog switch: IN low (CMD_EN pulled down, MCU in reset) -> D on S1 = 0 V; IN high -> D on S2 = amplifier */}
    <U n="U15" c="C6581" mpn="DG419DY-T1-E3" pins={["D", "S1", "GND", "VPOS", "VL", "IN", "VNEG", "S2"]}
      conn={{ D: "CMD_OUT", S1: "GND", GND: "GND", VPOS: "V15P", VL: "V5", IN: "CMD_EN", VNEG: "V15N", S2: "CMD_PRE" }}
      pwr={["VPOS", "VNEG", "VL"]} gnd={["GND"]} must={["IN"]}
      arr={{ leftSide: S(["IN", "S2", "S1"]), rightSide: S(["D"]), topSide: S(["VPOS", "VL"], "left-to-right"), bottomSide: S(["VNEG", "GND"], "left-to-right") }} />
    <C n="C55" v="100n50" a="V15P" b="GND" />
    <C n="C56" v="100n50" a="V15N" b="GND" />
    <C n="C57" v="100n" a="V5" b="GND" />
    <R n="R37" v="100k" a="CMD_EN" b="GND" />
    <U n="D13" c="C2848698" mpn="SMAJ15CA" pins={["T1", "T2"]} conn={{ T1: "CMD_OUT", T2: "GND" }}
      arr={{ topSide: S(["T1"], "left-to-right"), bottomSide: S(["T2"], "left-to-right") }} />

    {SILK.map(([t, x, y, fs]) => <silkscreentext text={t} pcbX={x} pcbY={y} fontSize={`${fs}mm`} />)}
  </board>
)
